from django.urls import path

from admins.views import index, UserCreateView, UserListView, UserUpdateView, admin_users_delete

app_name = 'baskets'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:id>/', admin_users_delete, name='admin_users_delete'),
]