from django.shortcuts import render
from django.http import HttpResponse
from mymedicine.models import Disease,Department,Medicine,Symptoms,DiseaseDepartment,DiseaseSymptom,DiseaseMedicine,DiseaseTreatment
from django.db.models import Q
def index(request):
    return render(request,'mymedicine/index.html')
def left(request):
    return render(request,'mymedicine/left.html')
def right(request):
    return render(request,'mymedicine/right.html')
def top(request):
    return render(request,'mymedicine/top.html')
def disease(request):
    alldiseases = Disease.objects.all()
    if request.method == "POST":
        btn = request.POST.get('delbtn','')
        if btn !='':
            Disease.objects.filter(Q(id=int(btn))).delete()
        name = request.POST.get('name','')
        altername = request.POST.get('altername', '')
        people = request.POST.get('people', '')
        infectivity = request.POST.get('infectivity','')
        under_insurance = request.POST.get('under_insurance','')
        if infectivity != '':
            diseases = Disease.objects.filter(Q(infectivity=int(infectivity)))
        else :
            diseases = Disease.objects.all()
        if under_insurance !='':
            diseases = diseases.filter(Q(infectivity=int(under_insurance)))
        if name!='':
            diseases =diseases.filter(Q(name=name))
        if altername != '':
            diseases =diseases.filter(Q(altername=altername))
        if people != '':
            diseases = diseases.filter(Q(people=people))
        detailbtn = request.POST.get('detailbtn','')
        if detailbtn !='':
            detaildisease = Disease.objects.get(Q(id=int(detailbtn)))
            disease_departments = DiseaseDepartment.objects.filter(Q(disease_id=int(detailbtn)))

            disease_symptons = DiseaseSymptom.objects.filter(Q(disease_id=int(detailbtn)))
            disease_medicines = DiseaseMedicine.objects.filter(Q(disease_id=int(detailbtn)))
            disease_treaments = DiseaseTreatment.objects.filter(Q(disease_id=int(detailbtn)))
            drug_list =[]
            symptom_list=[]
            dept_list = []
            treat_list = []
            for dept in disease_departments:
                dept_list.append(dept.department.department)
            for medicine in disease_medicines:
                drug_list.append(medicine.medicine.name)
            for sympoton in disease_symptons:
                symptom_list.append(sympoton.symptom.symptom)
            for treatment in disease_treaments:
                treat_list.append(treatment.treament.treatment)

            context = {'disease': detaildisease, 'symptom': symptom_list, 'drug': drug_list, 'dept': dept_list,'treat': treat_list}
            return render(request,'mymedicine/detaildisease.html',context)


    else :
        diseases = Disease.objects.all()
    return render(request, 'mymedicine/disease.html', {'diseases': diseases,'alldiseases':alldiseases})
def disease_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        altername =request.POST.get('altername','')
        people =request.POST.get('people','')
        infectivity = int(request.POST.get('infectivity'))
        under_insurance = int(request.POST.get('under_insurance'))
        new_disease = Disease(name=name,altername=altername,people=people,infectivity=infectivity,under_insurance=under_insurance)
        new_disease.save()
        diseases = Disease.objects.all()
        return render(request, 'mymedicine/disease.html', {'diseases': diseases})

    else :
        return render(request,'mymedicine/diseaseadd.html')
def disease_detail(request):
    if request.method == "POST":
        editbtn = request.POST.get('editbtn')
        if editbtn !='':
            disease = Disease.objects.get(id=int(editbtn))
            return render(request,'mymedicine/diseaseedit.html',{'disease':disease})
def disease_edit(request):
    if request.method == "POST":
        id = int(request.POST.get('id'))
        name = request.POST.get('name','')
        altername = request.POST.get('altername','')
        people = request.POST.get('people','')
        if name != '':
            Disease.objects.filter(id = id).update(name = name)
        if altername!='':
            Disease.objects.filter(id=id).update(altername=altername)
        if people !='':
            Disease.objects.filter(id = id).update(people=people)
        detaildisease = Disease.objects.get(Q(id=id))
        disease_departments = DiseaseDepartment.objects.filter(Q(disease_id=id))

        disease_symptons = DiseaseSymptom.objects.filter(Q(disease_id=id))
        disease_medicines = DiseaseMedicine.objects.filter(Q(disease_id=id))
        disease_treaments = DiseaseTreatment.objects.filter(Q(disease_id=id))
        drug_list = []
        symptom_list = []
        dept_list = []
        treat_list = []
        for dept in disease_departments:
            dept_list.append(dept.department.department)
        for medicine in disease_medicines:
            drug_list.append(medicine.medicine.name)
        for sympoton in disease_symptons:
            symptom_list.append(sympoton.symptom.symptom)
        for treatment in disease_treaments:
            treat_list.append(treatment.treament.treatment)

        context = {'disease': detaildisease, 'symptom': symptom_list, 'drug': drug_list, 'dept': dept_list,
                   'treat': treat_list}

        return render(request,'mymedicine/detaildisease.html',context)

# Create your views here.
