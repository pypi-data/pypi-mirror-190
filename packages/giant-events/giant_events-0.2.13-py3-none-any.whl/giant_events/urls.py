from django.urls import path

from .views import EventDetail, EventIndex

app_name = "giant_events"

urlpatterns = [
    path("", EventIndex.as_view(), name="index"),
    path("<slug:slug>/", EventDetail.as_view(), name="detail"),
]
