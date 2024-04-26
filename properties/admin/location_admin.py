from django import forms
from django.contrib import admin

from properties.models import Location


class LocationForm(forms.ModelForm):
    def clean_position(self):
        position = self.cleaned_data["position"]
        return position.replace(" ", "").strip()

    class Meta:
        model = Location
        fields = "__all__"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "priority")
    form = LocationForm
