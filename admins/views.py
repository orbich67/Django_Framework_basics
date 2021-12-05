from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from products.models import ProductCategory, Product
from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductEditForm, ProductCategoryEditForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'Geek Shop - Админ Панель'}
    return render(request, 'admins/index.html', context)


# Create
class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')
    success_message = 'Вы успешно создали пользователя!'
    template_name = 'admins/admin-users-create.html'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Geek Shop - Создание пользователя'
        return context


# Read
class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Geek Shop - Пользователи'
        return context


# Update
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    success_message = 'Данные успешно изменены!'
    template_name = 'admins/admin-users-update-delete.html'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Geek Shop - Обновление пользователя'
        return context


# Delete
class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.safe_delete()
        return HttpResponseRedirect(success_url)


def categories(request):
    title = 'админка/категории'
    categories_list = ProductCategory.objects.all()
    content = {
        'title': title,
        'objects': categories_list
    }
    return render(request, 'admins/categories.html', content)


def category_create(request):
    pass


def category_delete(request):
    pass


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'admins/category_update.html'
    success_url = reverse_lazy('admins:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__id=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'admins/products.html', content)


def product_create(request, category_id):
    title = 'товары/создание'
    category = get_object_or_404(ProductCategory, category_id=category_id)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admins:products', args=[category_id]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'product_form': product_form,
        'category': category,
    }

    return render(request, 'admins/product_update.html', context)


class CategoryProductsReadView(ListView):
    model = Product
    context_object_name = 'objects'
    template_name = 'admins/products.html'

    def get_queryset(self):
        filtered_products = Product.objects.filter(category__id=self.kwargs['category_id'])
        return filtered_products

    def get_context_data(self):
        context = super(CategoryProductsReadView, self).get_context_data()
        context['category'] = self.kwargs.get('category_id')
        return context


def product_read(request, pk):
    title = 'продукт/подробнее'
    product = get_object_or_404(Product, pk=pk)
    context = {'title': title, 'object': product, }

    return render(request, 'admins/product_read.html', context)


def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admins:products', args=[product.category.id]))

    context = {'title': title, 'product_to_delete': product}

    return render(request, 'admins/product_delete.html', context)


def product_update(request, pk):
    title = 'товары/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admins:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'product_form': edit_form
    }

    return render(request, 'admins/product_update.html', context)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_product_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
