from django.urls import path
from .views import (buy_item, item_page, success_page, 
                    cancel_page, buy_order, order_page)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="Stripe API",
        default_version="v1",
        description="Django + Stripe test task",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("buy/<int:id>/", buy_item),
    path("item/<int:id>/", item_page),
    path("success", success_page),
    path("cancel", cancel_page),
    path("buy-order/<int:id>/", buy_order),
    path("order/<int:id>/", order_page),
    path("", schema_view.with_ui("swagger", cache_timeout=0)),
]
