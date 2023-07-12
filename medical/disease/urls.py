from django.urls import path
from .views import index, diseases, disease

urlpatterns = [
    path('', index),
    path('diseases', diseases),
    path('disease/<int:id>', disease),
]