from django.urls import path

from .views import (
    ChangeLabelPage,
    CreateLabelPage,
    DeleteLabelPage,
    LabelsListPage,
)

app_name = 'labels'
urlpatterns = [
    path("", LabelsListPage.as_view(), name='labels_list'),
    path('create/', CreateLabelPage.as_view(), name='create'),
    path("<int:pk>/update/", ChangeLabelPage.as_view(), name='change'),
    path("<int:pk>/delete/", DeleteLabelPage.as_view(), name='delete'),
]
