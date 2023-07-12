from django.urls import path
from mymedicine.views import index

urlpatterns = [
        path('', index),

]