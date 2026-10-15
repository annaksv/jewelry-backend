from django.urls import path

from .views import MyRoutesView, RunClaimView, RunRouteView, SavedRouteDetailView

urlpatterns = [
    path("runs/<uuid:run_id>/route/", RunRouteView.as_view(), name="run-route"),
    path("runs/<uuid:run_id>/claim/", RunClaimView.as_view(), name="run-claim"),
    path("me/routes/", MyRoutesView.as_view(), name="my-routes"),
    path("routes/<uuid:route_id>/", SavedRouteDetailView.as_view(), name="saved-route"),
]
