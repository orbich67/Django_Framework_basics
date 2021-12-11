from django.urls import path

from admins.views import index, UserCreateView, UserListView, UserUpdateView, UserDeleteView
import admins.views as admins

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),

    path('categories/create/', admins.category_create, name='category_create'),
    path('categories/read/', admins.categories, name='categories'),
    path('categories/update/<int:pk>/', admins.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:category_id>/', admins.category_delete, name='category_delete'),

    path('products/create/category/<int:category_id>/', admins.product_create, name='product_create'),
    path('products/read/category/<int:category_id>/', admins.CategoryProductsReadView.as_view(), name='products'),
    path('products/read/<int:pk>/', admins.CategoryProductsReadView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', admins.product_update, name='product_update'),
    path('products/delete/<int:pk>/', admins.product_delete, name='product_delete'),
]
