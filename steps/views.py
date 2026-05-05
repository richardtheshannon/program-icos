import io
import json
from datetime import datetime

from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from steps.forms import StepWorkForm
from steps.models import Question, Response, Step, StepProgress

# V003.0 design tokens — forest-green / bone / ink palette per locked decision.
PDF_BONE = colors.HexColor("#f5f2ea")
PDF_INK = colors.HexColor("#0e0f0c")
PDF_INK_DIM = colors.HexColor("#5a5a55")
PDF_ACCENT = colors.HexColor("#2C5F3F")
PDF_LINE = colors.HexColor("#d8d2c1")


class StepListView(ListView):
    """Shows all 12 steps with per-user progress indicators."""

    model = Step
    template_name = "steps/step_list.html"
    context_object_name = "steps"

    def get_queryset(self) -> QuerySet[Step]:
        return Step.objects.prefetch_related("questions").all()

    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Find first incomplete step number
        current_step_found = False
        completed_count = 0

        # Build progress data for each step
        progress_map: dict = {}
        for step in context["steps"]:
            progress, _ = StepProgress.objects.get_or_create(
                user=user, step=step
            )
            total_questions = step.questions.count()
            answered = Response.objects.filter(
                user=user, question__step=step
            ).exclude(answer="").count()
            pct = int((answered / total_questions) * 100) if total_questions > 0 else 0

            is_current = False
            if not current_step_found and progress.status != StepProgress.Status.COMPLETE:
                is_current = True
                current_step_found = True

            if progress.status == StepProgress.Status.COMPLETE:
                completed_count += 1

            progress_map[step.pk] = {
                "progress": progress,
                "total_questions": total_questions,
                "answered": answered,
                "percentage": pct,
                "is_current": is_current,
            }

        context["progress_map"] = progress_map
        context["completed_count"] = completed_count
        context["meta_html"] = (
            f'<span class="num">{completed_count}</span> of <span class="num">12</span> complete'
        )
        return context


def step_detail_view(request: HttpRequest, step_number: int) -> HttpResponse:
    """Step detail page with question form. Handles GET (display) and POST (save)."""
    step = get_object_or_404(
        Step.objects.prefetch_related("questions"), number=step_number
    )

    # Get or create progress, mark as in_progress on first visit
    progress, created = StepProgress.objects.get_or_create(
        user=request.user, step=step
    )
    if progress.status == StepProgress.Status.NOT_STARTED:
        progress.status = StepProgress.Status.IN_PROGRESS
        progress.started_at = timezone.now()
        progress.save()

    # Previous / next step navigation
    prev_step = Step.objects.filter(number__lt=step.number).order_by("-number").first()
    next_step = Step.objects.filter(number__gt=step.number).order_by("number").first()

    if request.method == "POST":
        # Handle status change buttons
        new_status = request.POST.get("set_status")
        if new_status in ("complete", "revisiting"):
            progress.status = new_status
            if new_status == "complete":
                progress.completed_at = timezone.now()
            progress.save()
            label = "Complete" if new_status == "complete" else "Revisiting"
            messages.success(request, f"Step {step.number} marked as {label}.")
            return redirect("step_detail", step_number=step.number)

        # Handle form save
        form = StepWorkForm(request.POST, step=step, user=request.user)
        if form.is_valid():
            answered = form.save()
            messages.success(request, f"Progress saved — {answered} answers recorded.")
            return redirect("step_detail", step_number=step.number)
    else:
        form = StepWorkForm(step=step, user=request.user)

    # Build question-field pairs for template rendering
    questions = list(step.questions.all())
    question_fields = []
    for question in questions:
        field_name = f"q_{question.id}"
        question_fields.append({
            "question": question,
            "field": form[field_name],
            "field_name": field_name,
        })

    total_questions = len(questions)
    answered_count = Response.objects.filter(
        user=request.user, question__step=step
    ).exclude(answer="").count()
    percentage = int((answered_count / total_questions) * 100) if total_questions > 0 else 0

    eyebrow = f"STEP {step.number:02d} · {step.spiritual_principle.upper()}"
    meta_html = (
        f'<span class="num">{answered_count}</span> / '
        f'<span class="num">{total_questions}</span> answered'
    )

    return render(request, "steps/step_detail.html", {
        "step": step,
        "form": form,
        "question_fields": question_fields,
        "progress": progress,
        "prev_step": prev_step,
        "next_step": next_step,
        "total_questions": total_questions,
        "answered_count": answered_count,
        "percentage": percentage,
        "eyebrow": eyebrow,
        "meta_html": meta_html,
    })


@require_POST
def auto_save_response(request: HttpRequest) -> HttpResponse:
    """HTMX endpoint: auto-save a single question response."""
    question_id = request.POST.get("question_id")
    if not question_id:
        return JsonResponse({"error": "Missing question_id"}, status=400)

    question = get_object_or_404(Question, pk=question_id)
    field_name = f"q_{question_id}"
    answer = request.POST.get(field_name, "")

    Response.objects.update_or_create(
        user=request.user,
        question=question,
        defaults={"answer": answer},
    )

    # Update step progress if it was not_started
    progress, _ = StepProgress.objects.get_or_create(
        user=request.user, step=question.step
    )
    if progress.status == StepProgress.Status.NOT_STARTED:
        progress.status = StepProgress.Status.IN_PROGRESS
        progress.started_at = timezone.now()
        progress.save()

    return render(request, "steps/partials/save_indicator.html", {
        "saved": True,
        "state": "saved",
        "question_id": question_id,
    })


def _build_pdf_styles() -> dict[str, ParagraphStyle]:
    """Build reusable paragraph styles for PDF export.

    V003.0 palette: bone bg + forest-green accents/headings + ink body + Courier mono
    metadata. Times-Roman/Times-Italic serif for headings (matches the on-screen
    display-serif treatment); Helvetica for body (close to the on-screen Inter fallback);
    Courier for mono.
    """
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "StepTitle", parent=styles["Heading1"], fontName="Times-Roman",
            fontSize=22, leading=26, spaceAfter=4, textColor=PDF_ACCENT,
        ),
        "subtitle": ParagraphStyle(
            "StepSubtitle", parent=styles["Normal"], fontName="Times-Italic",
            fontSize=12, leading=16, spaceAfter=10, textColor=PDF_INK_DIM,
        ),
        "eyebrow": ParagraphStyle(
            "Eyebrow", parent=styles["Normal"], fontName="Courier",
            fontSize=8, leading=10, spaceAfter=8, textColor=PDF_INK_DIM,
        ),
        "heading": ParagraphStyle(
            "SectionHeading", parent=styles["Heading2"], fontName="Times-Roman",
            fontSize=13, leading=16, spaceBefore=6, spaceAfter=4,
            textColor=PDF_ACCENT,
        ),
        "body": ParagraphStyle(
            "BodyText", parent=styles["Normal"], fontName="Helvetica",
            fontSize=10, leading=14, spaceAfter=6, textColor=PDF_INK,
        ),
        "question": ParagraphStyle(
            "Question", parent=styles["Normal"], fontName="Helvetica-Bold",
            fontSize=10, leading=14, spaceBefore=8, spaceAfter=4,
            textColor=PDF_INK,
        ),
        "answer": ParagraphStyle(
            "Answer", parent=styles["Normal"], fontName="Helvetica",
            fontSize=10, leading=14, spaceAfter=12, leftIndent=20,
            textColor=PDF_INK,
        ),
        "italic": ParagraphStyle(
            "Italic", parent=styles["Normal"], fontName="Helvetica-Oblique",
            fontSize=10, leading=14, spaceAfter=8, textColor=PDF_INK_DIM,
        ),
        "doc_title": ParagraphStyle(
            "DocTitle", parent=styles["Heading1"], fontName="Times-Roman",
            fontSize=32, leading=38, spaceAfter=8, textColor=PDF_ACCENT,
        ),
    }


def _draw_chrome(canvas, doc, label: str = "PS01") -> None:
    """Page chrome: bone bg, forest-green hairline rule, mono header + footer."""
    canvas.saveState()
    # Bone-card page background.
    canvas.setFillColor(PDF_BONE)
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], stroke=0, fill=1)
    # Hairline rule under the eyebrow header.
    canvas.setStrokeColor(PDF_LINE)
    canvas.setLineWidth(0.5)
    rule_y = doc.pagesize[1] - 0.55 * inch
    canvas.line(0.75 * inch, rule_y, doc.pagesize[0] - 0.75 * inch, rule_y)
    # Eyebrow: PS01 wordmark in forest-green Courier.
    canvas.setFillColor(PDF_ACCENT)
    canvas.setFont("Courier-Bold", 8)
    canvas.drawString(0.75 * inch, doc.pagesize[1] - 0.45 * inch, label.upper())
    # Footer: page number + export date in dim ink Courier.
    canvas.setFillColor(PDF_INK_DIM)
    canvas.setFont("Courier", 8)
    page_num = canvas.getPageNumber()
    today = datetime.now().strftime("%Y-%m-%d")
    canvas.drawRightString(
        doc.pagesize[0] - 0.75 * inch, 0.45 * inch,
        f"PAGE {page_num}  ·  EXPORTED {today}",
    )
    canvas.restoreState()


def _build_step_content(
    step: Step, user: object, pdf_styles: dict[str, ParagraphStyle]
) -> list:
    """Build PDF story elements for a single step."""
    story: list = []
    story.append(Paragraph(f"STEP {step.number:02d}", pdf_styles["eyebrow"]))
    story.append(Paragraph(step.title, pdf_styles["title"]))
    story.append(Paragraph(f"Spiritual principle · {step.spiritual_principle}", pdf_styles["subtitle"]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(step.description, pdf_styles["body"]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Focus", pdf_styles["heading"]))
    story.append(Paragraph(step.focus, pdf_styles["body"]))
    story.append(Spacer(1, 0.2 * inch))

    questions = step.questions.all()
    responses = {
        r.question_id: r.answer
        for r in Response.objects.filter(user=user, question__step=step)
    }

    for q in questions:
        story.append(Paragraph(f"Q{q.number}. {q.text}", pdf_styles["question"]))
        answer = responses.get(q.pk, "")
        if answer:
            story.append(Paragraph(answer, pdf_styles["answer"]))
        else:
            story.append(Paragraph("<i>(not yet answered)</i>", pdf_styles["italic"]))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Recovery outcome", pdf_styles["heading"]))
    story.append(Paragraph(step.recovery_outcome, pdf_styles["body"]))
    return story


class StepExportView(View):
    """Export a single step as PDF."""

    def get(self, request: HttpRequest, step_number: int) -> HttpResponse:
        step = get_object_or_404(Step, number=step_number)
        pdf_styles = _build_pdf_styles()

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=letter,
            topMargin=0.95 * inch, bottomMargin=0.75 * inch,
            leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        )
        story = _build_step_content(step, request.user, pdf_styles)
        label = f"PS01 · STEP {step.number:02d}"
        doc.build(
            story,
            onFirstPage=lambda c, d: _draw_chrome(c, d, label),
            onLaterPages=lambda c, d: _draw_chrome(c, d, label),
        )

        buf.seek(0)
        response = HttpResponse(buf.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="step_{step.number}.pdf"'
        return response


class AllStepsExportView(View):
    """Export all 12 steps as a single PDF with page breaks."""

    def get(self, request: HttpRequest) -> HttpResponse:
        steps = Step.objects.prefetch_related("questions").all()
        pdf_styles = _build_pdf_styles()

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=letter,
            topMargin=0.95 * inch, bottomMargin=0.75 * inch,
            leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        )

        # Title page
        story: list = []
        story.append(Spacer(1, 1.6 * inch))
        story.append(Paragraph("PS01 · POWERFUL SILENCE", pdf_styles["eyebrow"]))
        story.append(Paragraph("My step work", pdf_styles["doc_title"]))
        story.append(Spacer(1, 0.4 * inch))
        story.append(Paragraph(
            f"Exported by {request.user.first_name or request.user.username}",
            pdf_styles["body"],
        ))
        story.append(PageBreak())

        # Table of contents
        story.append(Paragraph("CONTENTS", pdf_styles["eyebrow"]))
        story.append(Paragraph("Table of contents", pdf_styles["title"]))
        story.append(Spacer(1, 0.2 * inch))
        for step in steps:
            story.append(Paragraph(
                f"Step {step.number:02d} · {step.title}", pdf_styles["body"],
            ))
        story.append(PageBreak())

        # Each step
        for i, step in enumerate(steps):
            story.extend(_build_step_content(step, request.user, pdf_styles))
            if i < len(steps) - 1:
                story.append(PageBreak())

        doc.build(
            story,
            onFirstPage=lambda c, d: _draw_chrome(c, d, "PS01 · STEP WORK"),
            onLaterPages=lambda c, d: _draw_chrome(c, d, "PS01 · STEP WORK"),
        )
        buf.seek(0)
        response = HttpResponse(buf.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="all_steps.pdf"'
        return response
