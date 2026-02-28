from django import forms

from steps.models import Question, Response


class StepWorkForm(forms.Form):
    """Dynamic form that generates one field per question in a step.

    Field names use the pattern ``q_{question.id}`` so they can be mapped back
    to the corresponding Question/Response records on save.
    """

    def __init__(self, *args, step, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step
        self.user = user

        questions = step.questions.all()
        existing = {
            str(r.question_id): r.answer
            for r in Response.objects.filter(user=user, question__step=step)
        }

        for question in questions:
            field_name = f"q_{question.id}"
            initial = existing.get(str(question.id), "")

            widget_attrs = {
                "class": (
                    "w-full bg-ps-bg border border-ps-border rounded-lg px-4 py-3 "
                    "text-gray-200 placeholder-gray-500 focus:border-ps-accent "
                    "focus:ring-1 focus:ring-ps-accent focus:outline-none resize-y"
                ),
                "placeholder": "Write your thoughts here…",
            }

            if question.question_type == Question.QuestionType.LETTER:
                widget_attrs["rows"] = 8
            elif question.question_type == Question.QuestionType.LIST_BUILDER:
                widget_attrs["rows"] = 6
                widget_attrs["placeholder"] = "One item per line…"
            elif question.question_type == Question.QuestionType.ACTION_PLAN:
                widget_attrs["rows"] = 6
                widget_attrs["placeholder"] = "Describe your plan…"
            else:
                widget_attrs["rows"] = 4

            self.fields[field_name] = forms.CharField(
                required=False,
                initial=initial,
                widget=forms.Textarea(attrs=widget_attrs),
                label=question.text,
                help_text=question.help_text or "",
            )

    def save(self):
        """Persist answers as Response objects. Returns count of non-empty answers."""
        answered = 0
        for field_name, value in self.cleaned_data.items():
            if not field_name.startswith("q_"):
                continue
            question_id = field_name[2:]
            Response.objects.update_or_create(
                user=self.user,
                question_id=question_id,
                defaults={"answer": value},
            )
            if value.strip():
                answered += 1
        return answered
