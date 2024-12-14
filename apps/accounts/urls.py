from django.urls import path
from .views import register_view, login_view, profile_view, password_change_view, confirm_mail_view, status_email_view,index_view, logout_view  

urlpatterns = [
    path('',index_view, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('password-change/',password_change_view, name='password_change'),
    path('confirm-email/<str:code>/', confirm_mail_view, name='confirm_email'),
    path('status-email/<str:message>/', status_email_view, name='status_email'),
]