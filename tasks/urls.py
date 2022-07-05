from django.urls import path
from .views import (
    ChangeTaskPage,
    CreateTaskPage,
    DeleteTaskPage,
    TaskDetailPage,
    TasksListPage,
)

app_name = 'tasks'
urlpatterns = [
    path("", TasksListPage.as_view(), name='tasks_list'),
    path('create/', CreateTaskPage.as_view(), name='create'),
    path("<int:pk>/update/", ChangeTaskPage.as_view(), name='update'),
    path("<int:pk>/delete/", DeleteTaskPage.as_view(), name='delete'),
    path("<int:pk>/", TaskDetailPage.as_view(), name='details'),
]
