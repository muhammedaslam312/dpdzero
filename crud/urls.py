from django.urls import path

from .views import DataMultiView, DataView

urlpatterns = [
    path("data/", DataMultiView.as_view(), name="store_data"),
    path("data/<key>/", DataView.as_view(), name="data_view"),
]
