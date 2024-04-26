from django import forms
from django.contrib import admin

from properties.models import Location, Property


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "priority")

    def save_model(self, request, obj, form, change):
        obj.position = obj.position.replace(" ", "").strip()
        super().save_model(request, obj, form, change)


class PropertyForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Property.Tag.choices,
    )
    condition = forms.ChoiceField(
        required=False, widget=forms.RadioSelect,
        choices=Property.Condition.choices
    )

    class Meta:
        model = Location
        fields = '__all__'


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("reference", "zone", "price")
    form = PropertyForm
