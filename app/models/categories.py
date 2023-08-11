from django.db import models

from app.models.model_choices import CATEGORY_CHOICES, SALAD


class Category(models.Model):
    title = models.IntegerField(
        choices=CATEGORY_CHOICES,
        default=SALAD,
        unique=True,
        verbose_name="Category name",
    )

    image = models.ImageField(
        upload_to="categories_pics",
        verbose_name="Category picture",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_title_display()

    @property
    def category_items_count(self):
        foods = self.foodanddrinks_set.count
        return foods

    class Meta:
        db_table = "takeaway_categories"
        verbose_name_plural = "Categories"
