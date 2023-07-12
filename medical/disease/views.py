from django.shortcuts import render
from django.http import HttpResponse
from .models import Disease, Symptom, Department, Treatment, Drug

# Create your views here.

def index(request):
    return HttpResponse('This is a medical database.')

def diseases(request):
    diseases = Disease.objects.all()
    return render(request, 'diseases.html', {'diseases': diseases})

def disease(request, id, method=['GET']):
    disease = Disease.objects.get(id=id+20)
    symptom = list(Symptom.objects.filter(disease__id=id+20))
    symptom_list = [s.symptom for s in symptom]
    drug = list(Drug.objects.filter(disease__id=id+20))
    drug_list = [u.drug for u in drug]
    dept = list(Department.objects.filter(disease__id=id+20))
    dept_list = [p.department for p in dept]
    treat = list(Treatment.objects.filter(disease__id=id+20))
    treat_list = [t.treatment for t in treat]
    context = {'disease': disease, 'symptom': symptom_list, 'drug': drug_list, 'dept': dept_list, 'treat': treat_list}
    return render(request, 'disease.html', context)