from django import forms
from .models import SiteConfig

class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = ["site_name", "logo", "primary_color", "secondary_color"]
        widgets = {
            "primary_color": forms.TextInput(attrs={"type": "color"}),
            "secondary_color": forms.TextInput(attrs={"type": "color"}),
        }