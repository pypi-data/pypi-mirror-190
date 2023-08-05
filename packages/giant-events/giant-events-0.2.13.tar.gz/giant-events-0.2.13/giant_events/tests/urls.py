from django.urls import include, path

""""
Url patterns for testing
"""

urlpatterns = [path("events/", include("giant_events.urls", namespace="events"))]
