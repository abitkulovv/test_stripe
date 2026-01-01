from django.shortcuts import render
import stripe
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Item, Order
import os


stripe.api_key = settings.STRIPE_SECRET_KEY

render_url = os.getenv("RENDER_URL")


@swagger_auto_schema(
    method="get",
    operation_summary="Buy item",
    operation_description="Create Stripe Checkout Session for Item",
    responses={
        200: openapi.Response(
            description="Stripe session id",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "session_id": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)
@api_view(["GET"])
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
        success_url=f"{render_url}/success",
        cancel_url=f"{render_url}/cancel",
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


@swagger_auto_schema(
    method="get",
    operation_summary="Pay order",
    operation_description="Create Stripe Checkout Session for Order",
    responses={
        200: openapi.Response(
            description="Stripe session id",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "session_id": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)
@api_view(["GET"])
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
        success_url=f"{render_url}/success/",
        cancel_url=f"{render_url}/cancel/",
    )

    return JsonResponse({"session_id": session.id})


def order_page(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, "templates/order.html", {
        "order": order,
        "stripe_key": settings.STRIPE_PUBLISHABLE_KEY
    })