from django.shortcuts import render

from products.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page, never_cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(category_id):
    if settings.LOW_CACHE:
        key = f'category_{category_id}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category_id=category_id)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category_id=category_id)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True)


# @cache_page(3600)
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)


# @cache_page(3600)
def products(request, category_id=None, page=1):
    links_menu = get_links_menu()

    context = {'title': 'GeekShop - Каталог', 'categories': links_menu}
    if category_id:
        products = get_category(category_id)
    else:
        products = get_products()
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator
    return render(request, 'products/products.html', context)
