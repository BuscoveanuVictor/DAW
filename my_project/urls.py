from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def index(request):
    return render(request, 'aplication/index.html')

def render_index(request):
    return render(request, '')

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('debug/', include('debug_toolbar.urls')),

    path('shop/', include('apps.shop.urls')),
    path('shop/', render_index, name='shop'),

    path('accounts/', include('apps.accounts.urls')),
    path('accounts/', render_index, name='accounts'),
]


