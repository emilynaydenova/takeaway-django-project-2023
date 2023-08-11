from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path

from accounts.views import (
    UserLoginView,
    RegisterPage,
    EditProfileView,
    DeleteProfileView,
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", RegisterPage.as_view(), name="register"),
    path("edit_profile/<int:pk>/", EditProfileView.as_view(), name="edit profile"),
    path(
        "delete_profile/<int:pk>/", DeleteProfileView.as_view(), name="delete profile"
    ),
    path(
        "reset_password/",
        PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_complete",
    ),
    path(
        "password_change/",
        PasswordChangeView.as_view(template_name="accounts/password_change_form.html"),
        name="password_change",
    ),
    path(
        "password_change_done/",
        PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"),
        name="password_change_done",
    ),
]
# template_name='password_change_form.html',next_page="password_change_done"