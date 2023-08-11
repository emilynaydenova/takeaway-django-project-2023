from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from accounts.forms import (
    RegisterUserForm,
    LoginUserForm,
    EditProfileForm,
    DeleteProfileForm,
)
from accounts.models import Profile


# LoginRequiredMixin is used
class UserLoginView(LoginView):
    template_name = "accounts/login_page.html"
    form_class = LoginUserForm
    redirect_authenticated_user = True  # prevent auth.user from this page

    def get_success_url(self):
        #  if not customer -> next= django admin
        #  else-> next=..... making an order,
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse_lazy("admin:login")
        return reverse_lazy("home")


class RegisterPage(CreateView):
    template_name = "accounts/register_page.html"
    form_class = RegisterUserForm
    redirect_authenticated_user = True  # prevent auth.user from this page
    success_url = reverse_lazy("home")

    # it is called after success
    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        user = self.object
        request = self.request
        user.groups.add(Group.objects.get(name="Customers"))
        login(request, user)
        return result

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super(RegisterPage, self).get(*args, **kwargs)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    exclude = ("user",)
    form_class = EditProfileForm
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy("home")

    def get_object(self, *args, **kwargs):
        # load data or empty
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return profile


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = Profile
    exclude = ("user",)
    form_class = DeleteProfileForm
    template_name = "accounts/delete_profile.html"
    success_url = reverse_lazy("home")

    def get_object(self, *args, **kwargs):
        # load data or empty
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return profile
