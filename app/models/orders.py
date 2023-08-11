from django.contrib.auth import get_user_model
from django.db import models

from app.models import FoodAndDrinks
from app.models.model_choices import STATUS_CHOICES, DELIVERY_CHOICES, TAKEAWAY, NEW

UserModel = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        UserModel, blank=True, null=True, on_delete=models.SET_NULL
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=NEW,
    )

    delivery = models.IntegerField(
        choices=DELIVERY_CHOICES,
        default=TAKEAWAY,
    )

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        return self.save()

    @property
    def get_username(self):
        username = self.user
        return username

    @property
    def get_order_total(self):
        items = self.orderitem_set.all()
        if items:
            total = sum([item.get_total for item in items])
        else:
            total = 0
        return total

    @property
    def get_order_items_quantity(self):
        items = self.orderitem_set.all()
        if items:
            total = sum([item.quantity for item in items])
        else:
            total = 0
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    product = models.ForeignKey(
        FoodAndDrinks,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        blank=True,
        null=True,
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.product.title)


class DeliveringInfo(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)

    user = models.ForeignKey(
        UserModel, blank=True, null=True, on_delete=models.SET_NULL
    )

    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address
