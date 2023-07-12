from django.db import models

# Create your models here.

class Disease(models.Model):
    # 疾病映射类，包括疾病名、又名、患病人群、传染性、是否在医保范围等属性
    name = models.CharField(max_length=64)
    alias = models.CharField(max_length=128)
    patient = models.TextField()
    infection = models.BooleanField()
    insurance = models.BooleanField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Disease:{self.name}>'
    
class Symptom(models.Model):
    # 症状映射类，包括症状、部位的属性
    symptom = models.CharField(max_length=32)
    part = models.CharField(max_length=32)
    disease = models.ManyToManyField('Disease')

    def __str__(self):
        return self.symptom

class Department(models.Model):
    department = models.CharField(max_length=32)
    disease = models.ManyToManyField('Disease')

    def __str__(self):
        return self.department

class Treatment(models.Model):
    treatment = models.CharField(max_length=32)
    disease = models.ManyToManyField('Disease')

    def __str__(self):
        return self.treatment
    
class Drug(models.Model):
    drug = models.CharField(max_length=32)
    adverse_reaction = models.TextField()
    usage = models.TextField()
    disease = models.ManyToManyField('Disease')

    def __str__(self):
        return self.drug