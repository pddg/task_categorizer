from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.TaskListView.as_view(), name="list"),
    path('completed/', views.CompletedTaskListView.as_view(), name="completed-list"),
    path('answer/<int:task_id>/', views.AnswerView.as_view(), name="answer"),
]
