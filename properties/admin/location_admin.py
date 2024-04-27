from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

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
    readonly_fields = ("embed_map",)
    form = LocationForm

    def embed_map(self, obj):
        return mark_safe(
            f"""
            <iframe 
                src="https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=es&amp;q={obj.position}+({obj.name})&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"
                width="100%" 
                height="450" 
                frameborder="0" 
                style="border:0" 
                scrolling="no">
            </iframe>
        """
        )

    embed_map.short_description = "Map"
