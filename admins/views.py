from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from users.models import User
from admins.forms import UserAdminRegistrationForm


def index(request):
    context = {'title': 'Geek Shop - Админ Панель'}
    return render(request, 'admins/index.html', context)


# Create
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно создали пользователя!')
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegistrationForm()
    context = {'title': 'Geek Shop - Создание пользователей', 'form': form}
    return render(request, 'admins/admin-users-create.html', context)


# Read
def admin_users(request):
    context = {
        'title': 'Geek Shop - Пользователи',
        'users': User.objects.all(),
    }
    return render(request, 'admins/admin-users-read.html', context)


# Update
def admin_users_update(request):
    context = {'title': 'Geek Shop - Обновление пользователя'}
    return render(request, 'admins/admin-users-update-delete.html', context)


# Delete
def admin_users_delete(request):
    pass
