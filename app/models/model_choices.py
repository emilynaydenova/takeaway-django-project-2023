from django.utils.translation import gettext_lazy as _

SALAD = 1
SOUP = 2
MAIN_DISH = 3
DESSERT = 4
DRINKS = 5

CATEGORY_CHOICES = (
    (SALAD, _("Salads")),
    (SOUP, _("Soups")),
    (MAIN_DISH, _("Main Dishes")),
    (DESSERT, _("Desserts")),
    (DRINKS, _("Drinks")),
)

NEW = 1
PENDING = 2
APPROVED = 3
REJECTED = 4
DELIVERED = 5

STATUS_CHOICES = (
    (NEW, _("New")),
    (PENDING, _("Pending")),
    (APPROVED, _("Approved")),
    (REJECTED, _("Rejected")),
    (DELIVERED, _("Delivered")),
)

TAKEAWAY = 1
DELIVERY = 2

DELIVERY_CHOICES = (
    (TAKEAWAY, "Takeaway"),
    (DELIVERY, "Home Delivery"),
)
