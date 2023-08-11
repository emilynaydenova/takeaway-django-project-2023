from django.core.exceptions import ValidationError
from django.db import models

from app.models import Category


class FoodAndDrinks(models.Model):
    title = models.CharField(
        max_length=50,
        null=True,
        verbose_name="Food or Drink name",
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to="food_and_drinks_pics", blank=True, null=True, verbose_name="Picture"
    )

    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    is_active = models.BooleanField(default=False)

    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="From Category",
    )

    def __str__(self):
        return self.title

    # cleans price for Django admin
    def clean(self):
        if self.price < 0:
            raise ValidationError("Price must be positive.")

    class Meta:
        db_table = "takeaway_food_and_drinks"
        unique_together = ("title", "category")
        verbose_name_plural = "Food and Drinks"

    # likes = models.PositiveIntegerField()
    #   likes = models.ForeignKey('Likes', on_delete=models.CASCADE)


#
# class Likes(models.Model):
#
#
#     class Meta:
#         unique_together = (food_and_drinks_id, user_profile_id)
#
#     pass
