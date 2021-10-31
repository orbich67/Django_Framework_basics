from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm


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
def admin_users_update(request, id):
    selected_user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserAdminProfileForm(instance=selected_user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно изменены!')
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminProfileForm(instance=selected_user)

    context = {'title': 'Geek Shop - Обновление пользователя',
               'form': form,
               'selected_user': selected_user,
    }
    return render(request, 'admins/admin-users-update-delete.html', context)


# Delete
def admin_users_delete(request):
    pass
