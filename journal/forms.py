from django import forms

from journal.models import DailyInventory, GratitudeEntry


class DailyInventoryForm(forms.ModelForm):
    class Meta:
        model = DailyInventory
        fields = [
            "serenity_level",
            "was_resentful",
            "resentful_details",
            "was_selfish",
            "selfish_details",
            "was_dishonest",
            "dishonest_details",
            "did_pray",
            "did_meditate",
            "spiritual_notes",
            "mood",
            "additional_notes",
        ]
        widgets = {
            "serenity_level": forms.NumberInput(attrs={
                "type": "range", "min": "1", "max": "10", "step": "1",
            }),
            "mood": forms.NumberInput(attrs={
                "type": "range", "min": "1", "max": "10", "step": "1",
            }),
            "resentful_details": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "What happened? Who were you resentful toward?",
            }),
            "selfish_details": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "How were you selfish or self-seeking?",
            }),
            "dishonest_details": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Where were you dishonest?",
            }),
            "spiritual_notes": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Any reflections from prayer or meditation…",
            }),
            "additional_notes": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Anything else on your mind…",
            }),
        }


class GratitudeEntryForm(forms.ModelForm):
    class Meta:
        model = GratitudeEntry
        fields = ["entry"]
        widgets = {
            "entry": forms.TextInput(attrs={
                "placeholder": "What are you grateful for?",
                "autocomplete": "off",
            }),
        }
