from decimal import Decimal

from django import forms
from django.contrib import admin

from properties.models import Property


class PropertyForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Property.Tag.choices,
    )
    condition = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices=Property.Condition.choices,
    )

    def clean_position(self):
        position = self.cleaned_data["position"]
        return position.replace(" ", "").strip()

    def clean(self):
        cleaned_data = super().clean()

        m2 = cleaned_data.get("m2")
        built_m2 = cleaned_data.get("built_m2")
        price = cleaned_data.get("price")

        cleaned_data["price_per_m2"] = round(price / m2, 2)
        cleaned_data["price_per_built_m2"] = (
            round(price / built_m2, 2) if built_m2 else None
        )

        return cleaned_data

    class Meta:
        model = Property
        fields = "__all__"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("reference", "zone", "price", "price_per_m2")
    form = PropertyForm
