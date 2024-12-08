from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('instruments/', views.instruments_list, name='instruments_list'),
    #path('add-instrument/', views.add_instrument, name='add_instrument'),
    path('contact/', views.contact, name='contact'),
    path('instrument_form/', views.instrument_form, name='instrument_form'),
    path('FormFilerInstr/', views.FormFilerInstr, name='FormFilerInstr'),
]                    
