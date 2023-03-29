from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test

from .models import Client, Order

@user_passes_test(lambda u: u.is_superuser)
def client(request):
    clients = Client.objects.all()
    q = request.GET.get('q', None)
    if q:
        clients = Client.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q) | Q(phone__icontains=q))
    context = {
        'clients': clients
    }
    return render(request, 'client/client.html', context)

@user_passes_test(lambda u: u.is_superuser)
def client_detail(request, telegram_id):
    client = get_object_or_404(Client, telegram_id=telegram_id)
    orders = Order.objects.filter(client=client)
    context = {
        'client': client,
        'orders': orders
    }
    return render(request, 'client/client_detail.html', context)

@user_passes_test(lambda u: u.is_superuser)
def order_times(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_checked = True
    order.delivered = False
    order.save()
    messages.info(request, 'Buyurtma ozgartirildi!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@user_passes_test(lambda u: u.is_superuser)
def order_check(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_checked = True
    order.delivered = True
    order.save()
    messages.info(request, 'Buyurtma ozgartirildi!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

