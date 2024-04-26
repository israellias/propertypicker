from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _


class Location(models.Model):
    class Priority(models.TextChoices):
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"

    name = models.CharField(verbose_name=_("Name"))
    position = models.CharField(verbose_name=_("Position"))
    priority = models.CharField(choices=Priority.choices, default=Priority.HIGH, verbose_name=_("Priority"))

    @property
    def latitude(self):
        return self.position.split(",")[0]

    @property
    def longitude(self):
        return self.position.split(",")[1]


class Property(models.Model):
    class Condition(models.TextChoices):
        NEW_HOUSE = "new_house", _("New House")
        OLD_HOUSE = "old_house", _("Old House")
        LAND = "land", _("Land")
        LAND_WITH_CONSTRUCTION = "land_with_construction", _("Land with Construction")
        APARTMENT = "apartment", _("Apartment")

    class Tag(models.TextChoices):
        AVENUE = "avenue", _("Avenue")
        GATED_COMMUNITY = "gated_community", _("Gated Community")
        ASPHALT = "asphalt", _("Asphalt")

    reference = models.CharField(verbose_name=_("Reference"))
    phone = models.CharField(null=True, blank=True, verbose_name=_("Phone"))
    position = models.CharField(verbose_name=_("Position"))
    zone = models.CharField(null=True, blank=True, verbose_name=_("Zone"))
    condition = models.CharField(choices=Condition.choices, default=Condition.OLD_HOUSE, verbose_name=_("Condition"))
    tags = ArrayField(models.CharField(choices=Tag.choices), default=list, blank=True, verbose_name=_("Tags"))

    m2 = models.DecimalField(decimal_places=2, max_digits=20, verbose_name=_("m2"))
    built_m2 = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=20, verbose_name=_("Built m2"))

    price = models.DecimalField(decimal_places=2, max_digits=20, verbose_name=_("Price"))
    price_per_m2 = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=20,
                                       verbose_name=_("Price per m2"))
    price_per_built_m2 = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=20,
                                             verbose_name=_("Price per built m2"))

    meters_in_front = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=20,
                                          verbose_name=_("Meters in front"))

    notes = models.TextField(null=True, blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
