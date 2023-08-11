from django.contrib import admin

# Register your models here.
from app.models import Category, FoodAndDrinks
from app.models.orders import Order, OrderItem, DeliveringInfo


class FoodAndDrinksInline(admin.TabularInline):
    model = FoodAndDrinks
    fields = ("title", "is_active")
    verbose_name_plural = "Food And Drinks"
    fk_name = "category"
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (FoodAndDrinksInline,)
    list_display = (
        "title",
        "category_items_count",
        "is_active",
    )
    verbose_name_plural = "Categories"
    ordering = ("title",)


@admin.register(FoodAndDrinks)
class FoodAndDrinksAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "is_active",
    )
    verbose_name_plural = "Food and Drinks"
    ordering = (
        "category",
        "title",
    )
    search_fields = ("title",)
    list_filter = (
        "is_active",
        "category",
    )

    list_editable = ("price", "is_active")
    fieldsets = (
        (
            "Required information",
            {
                "description": "Should be placed",
                "fields": ("title", "category", "price", "is_active"),
            },
        ),
        (
            "Optional information",
            {
                "description": "May be empty",
                "fields": (
                    "image",
                    "description",
                ),
            },
        ),
    )


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    fields = ("quantity",)
    verbose_name_plural = "Order Items"
    fk_name = "order"
    extra = 0


class DeliveringInfoInline(admin.TabularInline):
    model = DeliveringInfo
    fields = ("address", "city")
    verbose_name_plural = "Delivery Address"
    fk_name = "order"
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (
        DeliveringInfoInline,
        OrderItemInline,
    )
    list_display = ("id", "user", "created_on", "status")
    fields = (
        "user",
        "status",
        "delivery",
    )
    ordering = ("created_on",)
    search_fields = ("status", "get_username")
    list_filter = ("status",)
    readonly_fields = (
        "user",
        "created_on",
    )
    list_editable = ("status",)
