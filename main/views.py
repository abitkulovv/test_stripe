from django.shortcuts import render
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Item, Order


stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_item(request, id):
    item = get_object_or_404(Item, id=id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": item.currency,
                "product_data": {
                    "name": item.name,
                    "description": item.description,
                },
                "unit_amount": item.price,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://127.0.0.1:8000/success",
        cancel_url="http://127.0.0.1:8000/cancel",
    )

    return JsonResponse({"session_id": session.id})


def item_page(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, "templates/item.html", {
        "item": item,
        "stripe_key": settings.STRIPE_PUBLISHABLE_KEY
    })


def success_page(request):
    return JsonResponse({"success": True})


def cancel_page(request):
    return JsonResponse({"success": False})


def buy_order(request, id):
    order = get_object_or_404(Order, id=id)
    items = order.items.all()

    if not items:
        return JsonResponse({"error": "Order is empty"}, status=400)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    line_items = []
    for item in items:
        line_items.append({
            "price_data": {
                "currency": item.currency,
                "product_data": {
                    "name": item.name,
                },
                "unit_amount": item.price,
            },
            "quantity": 1,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )

    return JsonResponse({"session_id": session.id})


def order_page(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, "templates/order.html", {
        "order": order,
        "stripe_key": settings.STRIPE_PUBLISHABLE_KEY
    })