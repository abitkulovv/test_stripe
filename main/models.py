from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.IntegerField() # в центах Stripe rules not mine
    currency = models.CharField(max_length=3, default="usd")

    def __str__(self):
        return self.name
    
    def display_price(self):
        return self.price / 100
    

class Order(models.Model):
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(item.price for item in self.items.all())

    def currency(self):
        return self.items.first().currency
    
    def display_total(self):
        return self.total_amount() / 100