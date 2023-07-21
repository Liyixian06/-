from django.contrib import admin
from django.urls import path, include
from medicine.views import index,graph,search,departsearch
urlpatterns = [
    path('index',index),
    path('graph',graph),
    path('search',search),
    path('departsearch',departsearch),

]
