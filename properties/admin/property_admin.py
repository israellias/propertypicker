from django import forms
from django.contrib import admin

from properties.models import Property
from properties.repositories.property_repository import PropertyRepository


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
    readonly_fields = ("directions",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        PropertyRepository(obj).fill_directions()

    def directions(self, obj):
        note = ""
        for direction in obj.directions.all():
            note += f"{direction.location.name}\n"
            for key, value in direction.route_data["routes"][0].items():
                if isinstance(value, dict):
                    value = str(value)
                note += f"{key}: {value}\n"
            note += "\n"
        return note

    directions.short_description = "Directions"
