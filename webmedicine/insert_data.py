import os
os.environ['DJANGO_SETTINGS_MODULE']="webmedicine.settings"

import django;django.setup()
from mymedicine.models import Disease, Symptoms, Department, Treatments, Medicine, DiseaseSymptom, DiseaseDepartment, DiseaseTreatment, DiseaseMedicine
import csv

name_list = []
alias_list = []
patient_list = []
infection_list = []
insurance_list = []

symptom_list = []
part_list = []
disease_name_list = []
disease_symptom_list = []

drug_list = []
reaction_list = []
usage_list = []
disease_name_list2 = []
disease_drug_list = []

dept_list = []
disease_name_list3 = []
disease_dept_list = []

treat_list = []
disease_name_list4 = []
disease_treat_list = []

with open('data/disease.csv', mode='r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            name_list.append(line['疾病名'])
            alias_list.append(line['又名'])
            patient_list.append(line['患病人群'])
            infection_list.append(True if line['传染性']=='有' else False)
            insurance_list.append(True if line['是否在医保范围']=='是' else False)
f.close()

with open('data/symptom.csv', mode='r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        symptom_list.append(line['症状'])
        part_list.append(line['部位'])
f.close()

with open('data/disease_symptom.csv', mode='r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        disease_name_list.append(line['疾病'])
        disease_symptom_list.append(line['症状'])
f.close()

with open('data/drug.csv', mode='r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        drug_list.append(line['药物名'])
        reaction_list.append(line['不良反应'])
        usage_list.append(line['用法用量'])
f.close()

with open('data/disease_drug.csv', mode='r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        disease_name_list2.append(line['疾病'])
        disease_drug_list.append(line['药物'])
f.close()

with open('data/department.csv', mode='r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        dept_list.append(line['科室名'])
f.close()

with open('data/disease_department.csv', mode='r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        disease_name_list3.append(line['疾病'])
        disease_dept_list.append(line['科室'])
f.close()

with open('data/treatment.csv', mode='r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        treat_list.append(line['治疗方式'])
f.close()

with open('data/disease_treatment.csv', mode='r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        disease_name_list4.append(line['疾病'])
        disease_treat_list.append(line['治疗'])
f.close()

def create_diseases():
    for name, alias, patient, infection, insurance in zip(name_list, alias_list, patient_list, infection_list, insurance_list):
         print(name, alias, patient, infection, insurance)
         disease = Disease(name=name, altername=alias, people=patient, infectivity=infection, under_insurance=insurance)
         disease.save()

def create_symptoms():
    for symptom, part in zip(symptom_list, part_list):
        print(symptom, part)
        symptoms = Symptoms(symptom=symptom, part=part)
        symptoms.save()

def create_disease_symptom():
    for disease_name, symptom_name in zip(disease_name_list, disease_symptom_list):
        print(disease_name, symptom_name)
        d = Disease.objects.get(name=disease_name)
        s = Symptoms.objects.get(symptom=symptom_name)
        disease_symptom = DiseaseSymptom(disease=d, symptom=s)
        disease_symptom.save()

def create_drugs():
    for drug_name, reaction, usage in zip(drug_list, reaction_list, usage_list):
        print(drug_name, reaction, usage)
        drug = Medicine(name=drug_name, adverse_reaction = reaction, instruction = usage)
        drug.save()

def create_disease_drug():
    for disease_name, drug_name in zip(disease_name_list2, disease_drug_list):
        print(disease_name, drug_name)
        d = Disease.objects.get(name=disease_name)
        u = Medicine.objects.get(name=drug_name)
        disease_medicine = DiseaseMedicine(disease=d, medicine=u)
        disease_medicine.save()

def create_dept():
    for dept_name in dept_list:
        print(dept_name)
        dept = Department(department=dept_name)
        dept.save()

def create_disease_dept():
    for disease_name, dept_name in zip(disease_name_list3, disease_dept_list):
        print(disease_name, dept_name)
        d = Disease.objects.get(name=disease_name)
        p = Department.objects.get(department=dept_name)
        disease_dept = DiseaseDepartment(disease=d, department=p)
        disease_dept.save()

def create_treatment():
    for treat_name in treat_list:
        print(treat_name)
        treat = Treatments(treatment=treat_name)
        treat.save()

def create_disease_treatment():
    for disease_name, treat_name in zip(disease_name_list4, disease_treat_list):
        print(disease_name, treat_name)
        d = Disease.objects.get(name=disease_name)
        t = Treatments.objects.get(treatment=treat_name)
        disease_treat = DiseaseTreatment(disease=d, treament=t)
        disease_treat.save()

if __name__ == '__main__':
     #create_diseases()
     #create_symptoms()
     #create_disease_symptom()
     #create_drugs()
     #create_disease_drug()
     #create_dept()
     #create_disease_dept()
     #create_treatment()
     create_disease_treatment()