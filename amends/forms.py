from django import forms

from amends.models import Amend, Person

TEXTAREA_CLASS = "w-full px-3 py-2 bg-ps-bg border border-ps-border rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-ps-accent"
INPUT_CLASS = "w-full px-3 py-2 bg-ps-bg border border-ps-border rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-ps-accent"
SELECT_CLASS = "w-full px-3 py-2 bg-ps-bg border border-ps-border rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-ps-accent"


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "relationship", "how_harmed", "willingness_level"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Person's name",
                "class": INPUT_CLASS,
            }),
            "relationship": forms.TextInput(attrs={
                "placeholder": "e.g. Family, Friend, Coworker, Ex-partner...",
                "class": INPUT_CLASS,
            }),
            "how_harmed": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Describe how you harmed this person...",
                "class": TEXTAREA_CLASS,
            }),
            "willingness_level": forms.Select(attrs={
                "class": SELECT_CLASS,
            }),
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
            "status": forms.Select(attrs={"class": SELECT_CLASS}),
            "anger_letter": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "Write your honest feelings here. This is for YOUR eyes only...",
                "class": TEXTAREA_CLASS,
            }),
            "apology_letter": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "Draft your amends letter...",
                "class": TEXTAREA_CLASS,
            }),
            "actionable_amends": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "What concrete actions can you take?",
                "class": TEXTAREA_CLASS,
            }),
            "sponsor_feedback": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "What did your sponsor say?",
                "class": TEXTAREA_CLASS,
            }),
            "post_amend_reflection": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "How did making the amend feel? What happened?",
                "class": TEXTAREA_CLASS,
            }),
        }
