from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('product',products),
    path('product/<int:pk>/<slug:slug>', porduct_detale),
    
]
