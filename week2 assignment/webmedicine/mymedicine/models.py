from django.db import models

class Disease(models.Model):
    name = models.CharField(max_length=255)
    altername = models.CharField(max_length=255, blank=True, null=True)
    people = models.CharField(max_length=255, blank=True, null=True)
    infectivity = models.IntegerField()
    under_insurance = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'disease'

class Department(models.Model):
    #id = models.IntegerField(primary_key=True)
    department = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'department'

class DiseaseDepartment(models.Model):
    #id = models.IntegerField(primary_key=True)
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE, )
    department = models.ForeignKey('Department', on_delete=models.CASCADE,)

    class Meta:
        managed = True
        db_table = 'disease_department'

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    adverse_reaction = models.CharField(max_length=255, blank=True, null=True)
    instruction = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'medicine'

class DiseaseMedicine(models.Model):
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE,)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE,)

    class Meta:
        managed = True
        db_table = 'disease_medicine'

class Symptoms(models.Model):
    #id = models.IntegerField(primary_key=True)
    symptom = models.CharField(max_length=255)
    part = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'symptoms'

class DiseaseSymptom(models.Model):
    #id = models.IntegerField(primary_key=True)
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE,)
    symptom = models.ForeignKey('Symptoms', on_delete=models.CASCADE,)

    class Meta:
        managed = True
        db_table = 'disease_symptom'

class Treatments(models.Model):
    treatment = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'treatments'

class DiseaseTreatment(models.Model):
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE,)
    treament = models.ForeignKey('Treatments', on_delete=models.CASCADE,)

    class Meta:
        managed = True
        db_table = 'disease_treatment'
