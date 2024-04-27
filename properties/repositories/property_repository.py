import datetime

import requests
from django.conf import settings

from properties.models import Location, Direction, Property


class PropertyRepository:
    def __init__(self, property):
        self.property: Property = property

    def fill_directions(self):
        locations = Location.objects.all()
        for location in locations:
            direction, created = Direction.objects.get_or_create(
                property=self.property,
                location=location,
            )
            if created:
                direction.route_data = self.google_maps_route(location)
                direction.save()

    def google_maps_route(self, location: Location):
        tomorrow_at_22 = (
            datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        ).replace(hour=22, minute=0, second=0)
        res = requests.post(
            "https://routes.googleapis.com/directions/v2:computeRoutes",
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
                "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.localizedValues,routes.distanceMeters",
            },
            json={
                "origin": {
                    "location": {
                        "latLng": {
                            "latitude": self.property.latitude,
                            "longitude": self.property.longitude,
                        }
                    }
                },
                "destination": {
                    "location": {
                        "latLng": {
                            "latitude": location.latitude,
                            "longitude": location.longitude,
                        }
                    }
                },
                "travelMode": "DRIVE",
                "routingPreference": "TRAFFIC_AWARE",
                "departureTime": tomorrow_at_22.isoformat(),
                "computeAlternativeRoutes": False,
                "routeModifiers": {
                    "avoidTolls": False,
                    "avoidHighways": False,
                    "avoidFerries": False,
                },
                "languageCode": "es-BO",
                "units": "METRIC",
            },
        )
        return res.json()
