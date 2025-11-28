from django.urls import path
from .views import AnalyzeTasksView, SuggestTasksView, ListTasksView, CreateTaskView

urlpatterns = [
    path('add/', CreateTaskView.as_view(), name='create-task'),
    path('all/', ListTasksView.as_view(), name='list-tasks'),

    path('analyze/', AnalyzeTasksView.as_view(), name='analyze-tasks'),
    path('suggest/', SuggestTasksView.as_view(), name='suggest-tasks'),
]
