from django import forms

from amends.models import Amend, Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "relationship", "how_harmed", "willingness_level"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Person's name",
            }),
            "relationship": forms.TextInput(attrs={
                "placeholder": "e.g. Family, Friend, Coworker, Ex-partner…",
            }),
            "how_harmed": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Describe how you harmed this person…",
            }),
            "willingness_level": forms.Select(),
        }


class AmendForm(forms.ModelForm):
    class Meta:
        model = Amend
        fields = [
            "status",
            "anger_letter",
            "apology_letter",
            "actionable_amends",
            "sponsor_feedback",
            "post_amend_reflection",
        ]
        widgets = {
            "status": forms.Select(),
            "anger_letter": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "Write your honest feelings here. This is for YOUR eyes only…",
            }),
            "apology_letter": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "Draft your amends letter…",
            }),
            "actionable_amends": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "What concrete actions can you take?",
            }),
            "sponsor_feedback": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "What did your sponsor say?",
            }),
            "post_amend_reflection": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "How did making the amend feel? What happened?",
            }),
        }
