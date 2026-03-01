from django import forms

from journal.models import DailyInventory


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
                "class": "w-full accent-ps-accent",
            }),
            "mood": forms.NumberInput(attrs={
                "type": "range", "min": "1", "max": "10", "step": "1",
                "class": "w-full accent-ps-accent",
            }),
            "resentful_details": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "What happened? Who were you resentful toward?",
                "class": "w-full px-3 py-2 bg-ps-bg border border-ps-border rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-ps-accent",
            }),
            "selfish_details": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "How were you selfish or self-seeking?",
                "class": "w-full px-3 py-2 bg-ps-bg border border-ps-border rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-ps-accent",
            }),
            "dishonest_details": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Where were you dishonest?",
                "class": "w-full px-3 py-2 bg-ps-bg border border-ps-border rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-ps-accent",
            }),
            "spiritual_notes": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Any reflections from prayer or meditation...",
                "class": "w-full px-3 py-2 bg-ps-bg border border-ps-border rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-ps-accent",
            }),
            "additional_notes": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Anything else on your mind...",
                "class": "w-full px-3 py-2 bg-ps-bg border border-ps-border rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-ps-accent",
            }),
        }
