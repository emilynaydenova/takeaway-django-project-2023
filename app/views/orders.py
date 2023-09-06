import logging
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    TemplateView,
)

from ..forms import CheckoutOrderForm, DeliveringInfoForm
from ..models import FoodAndDrinks
from ..models.model_choices import NEW, DELIVERY
from ..models.orders import Order, DeliveringInfo, OrderItem

logging.basicConfig(level=logging.DEBUG)


def get_or_create_order(user):
    try:
        return Order.objects.get(status=NEW, user=user, is_deleted=False)
    except Order.DoesNotExist:
        logging.info(f"A new order is created for {user} at {datetime.now()}")
        return Order.objects.create(status=NEW, user=user)


# if user is authenticated and not is_staff or is_superuser
class OrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "app/order.html"
    context_object_name = "order"
    success_url = reverse_lazy("foods by category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        order = get_or_create_order(user)
        context["order"] = order
        try:
            items = order.orderitem_set.all()
            context["items"] = items.order_by("id")
        except items.DoesNotExist:
            logging.info(f"No ordered items in order of {user} from {order.created_on}")

        return context

    # this is instead of @login_required -> dispatch from LoginRequiredMixin
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or user.is_staff or user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OrderCheckoutView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = "app/checkout.html"
    form_class = CheckoutOrderForm
    context_object_name = "order"

    def get_success_url(self):
        # Home Delivery

        if self.object.delivery == DELIVERY:
            delivery = DeliveringInfo.objects.create(
                user=self.request.user,
                order=self.object,
            )
            return reverse_lazy("order delivering", kwargs={"pk": delivery.pk})
        # else - Takeaway
        return reverse_lazy(
            "order sheet", kwargs={"pk": self.object.pk}
        )  # 'order sheet' for pdf

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.orderitem_set.all()
        context["items"] = items
        return context


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = "app/order_delete.html"
    success_url = reverse_lazy("home")


# https://spapas.github.io/2015/11/27/pdf-in-django/
class OrderSheetView(LoginRequiredMixin, TemplateView):
    model = Order
    template_name = "app/order_sheet.html"
    context_object_name = "order"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs["pk"]
        context["order"] = Order.objects.get(pk=order_id)
        context["items"] = OrderItem.objects.filter(order_id=order_id).all()
        try:
            context["delivery"] = DeliveringInfo.objects.get(order_id=order_id)
        except DeliveringInfo.DoesNotExist:
            pass
        return context


class DeliveringInfoCreateView(LoginRequiredMixin, UpdateView):
    model = DeliveringInfo
    template_name = "app/delivering.html"
    form_class = DeliveringInfoForm
    context_object_name = "delivery"

    def get_success_url(self, **kwargs):
        order_id = self.object.order_id
        return reverse_lazy("order sheet", kwargs={"pk": order_id})


class OrderItemDeleteView(LoginRequiredMixin, DeleteView):
    model = OrderItem
    template_name = "app/confirm_delete.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy("order")


#  Login required!
def items_qty_plus(request, pk):
    item = OrderItem.objects.get(pk=pk)
    item.quantity += 1
    item.save()
    return redirect('order')


#  Login required!
def items_qty_minus(request, pk):
    item = OrderItem.objects.get(pk=pk)
    if item.quantity > 1:
        item.quantity -= 1
    item.save()
    return redirect('order')


#  Login required!
def order_item_add(request):
    user = request.user
    order = get_or_create_order(user)

    product_id = request.GET.get("food", None)
    product = FoodAndDrinks.objects.get(id=product_id)

    for item in order.orderitem_set.all():
        if item.product_id == product.id:
            item.quantity += 1
            item.save()
            break
    else:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1, )

    return redirect('order')
