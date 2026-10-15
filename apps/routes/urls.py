from django.urls import path

from .views import RunRouteView

urlpatterns = [
    path("runs/<uuid:run_id>/route/", RunRouteView.as_view(), name="run-route"),
]
