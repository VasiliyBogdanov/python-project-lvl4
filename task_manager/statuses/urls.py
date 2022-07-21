from django.urls import path

from . import views

app_name = 'statuses'
urlpatterns = [
    path("", views.StatusesListPage.as_view(), name='statuses_list'),
    path('create/', views.CreateStatusPage.as_view(), name='create'),
    path('<int:pk>/update/', views.ChangeStatusPage.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteStatusPage.as_view(), name='delete'),
]
