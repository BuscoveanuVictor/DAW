from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('instruments/', views.instruments_list, name='instruments_list'),
    path('contact/', views.contact, name='contact'),
    path('add_instrument/', views.add_instrument, name='add_instrument'),
    path('filter/', views.filter, name='filter'),
]                    
