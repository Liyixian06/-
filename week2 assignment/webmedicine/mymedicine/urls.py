from django.urls import path
from mymedicine.views import index,disease,disease_add,left,top,right,disease_edit,disease_detail

urlpatterns = [
        path('index', index),
        path('disease', disease),
        path('diseaseadd',disease_add),
        path('diseaseedit',disease_edit),
        path('detaildisease',disease_detail),
        path('left',left),
        path('right',right),
        path('top',top),

]