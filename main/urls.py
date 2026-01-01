from django.urls import path
from .views import (buy_item, item_page, success_page, 
                    cancel_page, buy_order, order_page)


urlpatterns = [
    path("buy/<int:id>/", buy_item),
    path("item/<int:id>/", item_page),
    path("success", success_page),
    path("cancel", cancel_page),
    path("buy-order/<int:id>/", buy_order),
    path("order/<int:id>/", order_page),
]
