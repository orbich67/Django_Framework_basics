from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from products.models import Product
from baskets.models import Basket
from django.db.models import F, Q


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)

    old_basket_items = Basket.objects.filter(user=request.user, product=product)

    if not old_basket_items.exists():
        Basket.objects.create(user=request.user, product=product)

    if old_basket_items:
        old_basket_items[0].quantity += 1
        old_basket_items[0].save()
    else:
        old_basket_items[0].quantity = F('quantity') + 1

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
    baskets = Basket.objects.filter(user=request.user)
    context = {'baskets': baskets}
    result = render_to_string('baskets/baskets.html', context)
    return JsonResponse({'result': result})
