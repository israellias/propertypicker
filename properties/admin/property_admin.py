import re

import googlemaps
from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

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
        if re.match(r"\b[\w]{2,4}\+[\w]{2,4}\b(?:\s+[A-Za-z\s]+)?", position):
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            geocode = gmaps.geocode(position)
            return "{},{}".format(
                geocode[0]["geometry"]["location"]["lat"],
                geocode[0]["geometry"]["location"]["lng"],
            )

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
        fields = (
            "url",
            "reference",
            "position",
            "m2",
            "price",
            "phone",
            "zone",
            "condition",
            "tags",
            "built_m2",
            "price_per_m2",
            "price_per_built_m2",
            "meters_in_front",
            "notes",
        )


class TagsListFilter(admin.SimpleListFilter):
    title = "Tags"
    parameter_name = "tags"

    def lookups(self, request, model_admin):
        tags = Property.objects.values_list("tags", flat=True)
        tags = [(kw, kw) for sublist in tags for kw in sublist if kw]
        tags = sorted(set(tags))
        return tags

    def queryset(self, request, queryset):
        lookup_value = self.value()
        if lookup_value:
            queryset = queryset.filter(tags__contains=[lookup_value])
        return queryset


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "zone",
        "formatted_price",
        "price_per_m2",
        "route_notes",
    )
    form = PropertyForm
    readonly_fields = ("directions_explained", "embed_map")
    list_filter = ("zone", "condition", TagsListFilter)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        PropertyRepository(obj).fill_directions()

    def formatted_price(self, obj):
        return "{:0,.0f} USD".format(obj.price)

    formatted_price.short_description = "Price"

    def directions_explained(self, obj):
        note = ""
        for direction in obj.directions.all():
            note += f"{direction.location.name}\n"
            for key, value in direction.route_data["routes"][0].items():
                if isinstance(value, dict):
                    value = str(value)
                note += f"{key}: {value}\n"
            note += "\n"
        return note

    directions_explained.short_description = "Directions"

    def route_notes(self, obj):
        notes = [
            f"{direction.location.name}\n{direction.route_data['routes'][0]['localizedValues']['duration']['text']}"
            for direction in obj.directions.all()
        ]
        return " | ".join(notes)

    route_notes.short_description = "Directions"

    def embed_map(self, obj):
        return mark_safe(
            f"""
            <iframe 
                src="https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=es&amp;q={obj.position}+({obj.reference})&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"
                width="100%" 
                height="450" 
                frameborder="0" 
                style="border:0" 
                scrolling="no">
            </iframe>
        """
        )

    embed_map.short_description = "Map"
