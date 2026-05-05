import datetime
import io

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from journal.forms import DailyInventoryForm, GratitudeEntryForm
from journal.models import DailyInventory, GratitudeEntry

# V003.0 design tokens — same palette as steps/views.py.
PDF_BONE = colors.HexColor("#f5f2ea")
PDF_INK = colors.HexColor("#0e0f0c")
PDF_INK_DIM = colors.HexColor("#5a5a55")
PDF_ACCENT = colors.HexColor("#2C5F3F")
PDF_LINE = colors.HexColor("#d8d2c1")


class DailyCheckinView(View):
    """GET: show today's (or a specific date's) check-in form. POST: save it."""

    def get(self, request: HttpRequest, date: str | None = None) -> HttpResponse:
        checkin_date = self._parse_date(date)
        inventory = DailyInventory.objects.filter(
            user=request.user, date=checkin_date
        ).first()
        form = DailyInventoryForm(instance=inventory)
        streak = DailyInventory.current_streak(request.user)
        meta_html = (
            f'<span class="num">{streak}</span> DAY STREAK' if streak > 0 else ""
        )
        return render(request, "journal/daily_checkin.html", {
            "form": form,
            "checkin_date": checkin_date,
            "is_today": checkin_date == timezone.now().date(),
            "inventory": inventory,
            "streak": streak,
            "meta_html": meta_html,
        })

    def post(self, request: HttpRequest, date: str | None = None) -> HttpResponse:
        checkin_date = self._parse_date(date)
        inventory = DailyInventory.objects.filter(
            user=request.user, date=checkin_date
        ).first()
        form = DailyInventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.date = checkin_date
            obj.save()
            messages.success(request, f"Check-in for {checkin_date} saved.")
            return redirect("daily_checkin")
        streak = DailyInventory.current_streak(request.user)
        meta_html = (
            f'<span class="num">{streak}</span> DAY STREAK' if streak > 0 else ""
        )
        return render(request, "journal/daily_checkin.html", {
            "form": form,
            "checkin_date": checkin_date,
            "is_today": checkin_date == timezone.now().date(),
            "inventory": inventory,
            "streak": streak,
            "meta_html": meta_html,
        })

    def _parse_date(self, date_str: str | None) -> datetime.date:
        if date_str:
            try:
                return datetime.date.fromisoformat(date_str)
            except ValueError:
                pass
        return timezone.now().date()


class JournalHistoryView(ListView):
    """Paginated list of past daily inventories."""

    model = DailyInventory
    template_name = "journal/history.html"
    context_object_name = "entries"
    paginate_by = 14

    def get_queryset(self):
        return DailyInventory.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        total = DailyInventory.objects.filter(user=self.request.user).count()
        context["total_count"] = total
        context["meta_html"] = f'<span class="num">{total}</span> entr{"y" if total == 1 else "ies"}'
        return context


class StreakView(View):
    """Streak surface — page-hero + bone-card with display-serif streak count."""

    def get(self, request: HttpRequest) -> HttpResponse:
        streak = DailyInventory.current_streak(request.user)
        return render(request, "journal/streak.html", {
            "streak": streak,
        })


class GratitudeView(View):
    """Today's gratitude list with inline add form."""

    def get(self, request: HttpRequest) -> HttpResponse:
        today = timezone.now().date()
        entries = GratitudeEntry.objects.filter(user=request.user, date=today)
        form = GratitudeEntryForm()
        return render(request, "journal/gratitude.html", {
            "entries": entries,
            "form": form,
            "gratitude_date": today,
        })


class GratitudeAddView(View):
    """HTMX POST: add a gratitude entry and return the updated list."""

    def post(self, request: HttpRequest) -> HttpResponse:
        today = timezone.now().date()
        form = GratitudeEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.date = today
            # Set order to next available
            max_order = (
                GratitudeEntry.objects.filter(user=request.user, date=today)
                .order_by("-order")
                .values_list("order", flat=True)
                .first()
            ) or 0
            entry.order = max_order + 1
            entry.save()
        # Return the full entry list partial for HTMX swap
        entries = GratitudeEntry.objects.filter(user=request.user, date=today)
        return render(request, "journal/partials/gratitude_list.html", {
            "entries": entries,
            "form": GratitudeEntryForm(),
        })


class GratitudeDeleteView(View):
    """HTMX DELETE: remove a gratitude entry and return the updated list."""

    def delete(self, request: HttpRequest, pk: str) -> HttpResponse:
        today = timezone.now().date()
        GratitudeEntry.objects.filter(pk=pk, user=request.user).delete()
        entries = GratitudeEntry.objects.filter(user=request.user, date=today)
        return render(request, "journal/partials/gratitude_list.html", {
            "entries": entries,
            "form": GratitudeEntryForm(),
        })


class GratitudeHistoryView(ListView):
    """Browse past gratitude entries grouped by date."""

    model = GratitudeEntry
    template_name = "journal/gratitude_history.html"
    context_object_name = "entries"
    paginate_by = 50

    def get_queryset(self):
        return (
            GratitudeEntry.objects.filter(user=self.request.user)
            .order_by("-date", "order")
        )

    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        # Group entries by date for display
        entries = context["entries"]
        grouped: dict[datetime.date, list[GratitudeEntry]] = {}
        for entry in entries:
            grouped.setdefault(entry.date, []).append(entry)
        context["grouped_entries"] = dict(sorted(grouped.items(), reverse=True))
        total = GratitudeEntry.objects.filter(user=self.request.user).count()
        context["total_count"] = total
        context["meta_html"] = f'<span class="num">{total}</span> entr{"y" if total == 1 else "ies"}'
        return context


def _build_journal_pdf_styles() -> dict[str, ParagraphStyle]:
    """V003.0 palette — bone bg + forest-green serif headings + ink Helvetica body + Courier mono metadata."""
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title", parent=styles["Heading1"], fontName="Times-Roman",
            fontSize=22, leading=26, spaceAfter=4, textColor=PDF_ACCENT,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=styles["Normal"], fontName="Times-Italic",
            fontSize=12, leading=16, spaceAfter=14, textColor=PDF_INK_DIM,
        ),
        "eyebrow": ParagraphStyle(
            "Eyebrow", parent=styles["Normal"], fontName="Courier",
            fontSize=8, leading=10, spaceAfter=8, textColor=PDF_INK_DIM,
        ),
        "heading": ParagraphStyle(
            "Heading", parent=styles["Heading2"], fontName="Times-Roman",
            fontSize=13, leading=16, spaceBefore=8, spaceAfter=4,
            textColor=PDF_ACCENT,
        ),
        "body": ParagraphStyle(
            "Body", parent=styles["Normal"], fontName="Helvetica",
            fontSize=10, leading=14, spaceAfter=4, textColor=PDF_INK,
        ),
        "label": ParagraphStyle(
            "Label", parent=styles["Normal"], fontName="Helvetica-Bold",
            fontSize=10, leading=14, spaceAfter=2, textColor=PDF_INK,
        ),
        "meta": ParagraphStyle(
            "Meta", parent=styles["Normal"], fontName="Courier",
            fontSize=8, leading=10, spaceAfter=8, textColor=PDF_INK_DIM,
        ),
    }


def _draw_journal_chrome(canvas, doc, label: str = "PS01 · JOURNAL") -> None:
    """Page chrome: bone bg + forest-green hairline + Courier eyebrow header + dim Courier footer."""
    canvas.saveState()
    canvas.setFillColor(PDF_BONE)
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], stroke=0, fill=1)
    canvas.setStrokeColor(PDF_LINE)
    canvas.setLineWidth(0.5)
    rule_y = doc.pagesize[1] - 0.55 * inch
    canvas.line(0.75 * inch, rule_y, doc.pagesize[0] - 0.75 * inch, rule_y)
    canvas.setFillColor(PDF_ACCENT)
    canvas.setFont("Courier-Bold", 8)
    canvas.drawString(0.75 * inch, doc.pagesize[1] - 0.45 * inch, label.upper())
    canvas.setFillColor(PDF_INK_DIM)
    canvas.setFont("Courier", 8)
    page_num = canvas.getPageNumber()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    canvas.drawRightString(
        doc.pagesize[0] - 0.75 * inch, 0.45 * inch,
        f"PAGE {page_num}  ·  EXPORTED {today}",
    )
    canvas.restoreState()


class JournalExportView(View):
    """Export daily inventory entries for a date range as PDF."""

    def get(self, request: HttpRequest) -> HttpResponse:
        # Parse date range from query params (default: last 30 days)
        today = timezone.now().date()
        start_str = request.GET.get("start", "")
        end_str = request.GET.get("end", "")

        try:
            start_date = datetime.date.fromisoformat(start_str) if start_str else today - datetime.timedelta(days=30)
        except ValueError:
            start_date = today - datetime.timedelta(days=30)
        try:
            end_date = datetime.date.fromisoformat(end_str) if end_str else today
        except ValueError:
            end_date = today

        entries = DailyInventory.objects.filter(
            user=request.user, date__gte=start_date, date__lte=end_date
        ).order_by("-date")

        pdf_styles = _build_journal_pdf_styles()

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=letter,
            topMargin=0.95 * inch, bottomMargin=0.75 * inch,
            leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        )

        username = request.user.first_name or request.user.username
        story: list = []
        story.append(Paragraph(
            f"PS01 · {username.upper()} · DAILY INVENTORY",
            pdf_styles["eyebrow"],
        ))
        story.append(Paragraph("Daily inventory journal", pdf_styles["title"]))
        story.append(Paragraph(
            f"{start_date.strftime('%B %d, %Y')} – {end_date.strftime('%B %d, %Y')}",
            pdf_styles["subtitle"],
        ))
        story.append(Spacer(1, 0.2 * inch))

        if not entries:
            story.append(Paragraph("No entries found for this date range.", pdf_styles["body"]))
        else:
            for entry in entries:
                story.append(Paragraph(
                    entry.date.strftime("%A, %B %d, %Y"), pdf_styles["heading"],
                ))
                story.append(Paragraph(
                    f"SERENITY {entry.serenity_level}/10  ·  MOOD {entry.mood}/10",
                    pdf_styles["meta"],
                ))

                if entry.was_resentful:
                    story.append(Paragraph("Resentful: yes", pdf_styles["label"]))
                    if entry.resentful_details:
                        story.append(Paragraph(entry.resentful_details, pdf_styles["body"]))
                if entry.was_selfish:
                    story.append(Paragraph("Selfish: yes", pdf_styles["label"]))
                    if entry.selfish_details:
                        story.append(Paragraph(entry.selfish_details, pdf_styles["body"]))
                if entry.was_dishonest:
                    story.append(Paragraph("Dishonest: yes", pdf_styles["label"]))
                    if entry.dishonest_details:
                        story.append(Paragraph(entry.dishonest_details, pdf_styles["body"]))

                practices = []
                if entry.did_pray:
                    practices.append("Prayed")
                if entry.did_meditate:
                    practices.append("Meditated")
                if practices:
                    story.append(Paragraph(f"Practices: {', '.join(practices)}", pdf_styles["body"]))
                if entry.spiritual_notes:
                    story.append(Paragraph("Spiritual notes:", pdf_styles["label"]))
                    story.append(Paragraph(entry.spiritual_notes, pdf_styles["body"]))
                if entry.additional_notes:
                    story.append(Paragraph("Notes:", pdf_styles["label"]))
                    story.append(Paragraph(entry.additional_notes, pdf_styles["body"]))

                story.append(Spacer(1, 0.2 * inch))

        label = f"PS01 · JOURNAL · {username.upper()}"
        doc.build(
            story,
            onFirstPage=lambda c, d: _draw_journal_chrome(c, d, label),
            onLaterPages=lambda c, d: _draw_journal_chrome(c, d, label),
        )
        buf.seek(0)
        response = HttpResponse(buf.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="journal_export.pdf"'
        return response
