from django.urls import path

from .views import RunAnswerView, RunCreateView, RunDetailView, ScenarioDetailView, ScenarioListView

urlpatterns = [
    path("scenarios/", ScenarioListView.as_view(), name="scenario-list"),
    path("scenarios/<slug:slug>/", ScenarioDetailView.as_view(), name="scenario-detail"),
    path("runs/", RunCreateView.as_view(), name="run-create"),
    path("runs/<uuid:run_id>/", RunDetailView.as_view(), name="run-detail"),
    path("runs/<uuid:run_id>/answers/", RunAnswerView.as_view(), name="run-answers"),
]
