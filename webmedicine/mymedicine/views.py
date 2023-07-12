from django.shortcuts import render
from django.http import HttpResponse
from mymedicine.models import Disease,Department,Medicine,Symptoms
def index(request):

    return  HttpResponse('Hello World')

def disease(request):
    diseases = Disease.objects.all()
    return render(request, 'mymedicine/disease.html', {'diseases': diseases})

# Create your views here.
