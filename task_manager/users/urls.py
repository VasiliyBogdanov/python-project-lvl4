from django.urls import path

from . import views

USERS_LIST = 'users_list'
CREATE_USER = 'create_user'
UPDATE_USER = 'update'
DELETE_USER = 'delete'

app_name = 'users'
urlpatterns = [
    path('', views.UserListView.as_view(), name=USERS_LIST),
    path('create/', views.CreateUserView.as_view(), name=CREATE_USER),
    path('<int:pk>/update/', views.ChangeUser.as_view(), name=UPDATE_USER),
    path('<int:pk>/delete/', views.DeleteUser.as_view(), name=DELETE_USER),
]
