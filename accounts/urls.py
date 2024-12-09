from django.urls import path
from .views import register_view, login_view, profile_view
from django.contrib.auth.views import LogoutView, PasswordChangeView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='/profile/'
    ), name='password_change'),
]