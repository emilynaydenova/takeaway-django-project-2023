from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView

from app.models import Category, FoodAndDrinks


# Create your views here.


class IndexView(ListView):
    # has only one method - get()

    template_name = "index.html"  # from TemplateResponseMixin
    model = Category
    context_object_name = "categories"
    ordering = ("title",)

    # context
    # def get_context_data(self, **kwargs):  # from ContextMixin
    #     context = super().get_context_data(**kwargs)
    #
    #     context['title'] = "Class-Based with TemplateView"
    #     return context

class FoodsByCategoryListView(ListView):
    NUMBER_PER_PAGE = 4

    model = FoodAndDrinks
    template_name = "app/foods_by_category.html"
    context_object_name = "foods"
    ordering = ("title",)
    paginate_by = NUMBER_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get query parameter from url ?category="..."
        try:
            category_id = self.request.GET.get("category", None)
            context["category"] = Category.objects.get(id=category_id)
            return context
        except self.model.DoesNotExist:
            raise Http404("Not Found Such Category")

    def get_queryset(self):
        queryset = super().get_queryset()
        # filter foods by category and being active
        try:
            category_id = self.request.GET.get("category", None)
            queryset = queryset.filter(is_active=True, category_id=category_id)
            return queryset
        except self.model.DoesNotExist:
            raise Http404("Not Found Such Category")

    def get_allow_empty(self):
        self.allow_empty = True
        return self.allow_empty


class FoodDetailsView(DetailView):
    model = FoodAndDrinks
    template_name = "app/food_details.html"
    context_object_name = "food"

    def get_success_url(self):
        return reverse_lazy("foods by category")
