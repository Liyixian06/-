


from django.db import models


class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    department = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'department'


class Disease(models.Model):
    name = models.CharField(max_length=255)
    altername = models.CharField(max_length=255, blank=True, null=True)
    people = models.CharField(max_length=255, blank=True, null=True)
    infectivity = models.IntegerField()
    under_insurance = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'disease'


class DiseaseDepartment(models.Model):
    id = models.IntegerField(primary_key=True)
    disease = models.ForeignKey(Disease, models.DO_NOTHING)
    department = models.ForeignKey(Department, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'disease_department'


class DiseaseMedicine(models.Model):
    disease = models.ForeignKey(Disease, models.DO_NOTHING)
    medicine = models.ForeignKey('Medicine', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'disease_medicine'


class DiseaseSymptom(models.Model):
    id = models.IntegerField(primary_key=True)
    disease = models.ForeignKey(Disease, models.DO_NOTHING)
    symptom = models.ForeignKey('Symptoms', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'disease_symptom'


class DiseaseTreatment(models.Model):
    disease = models.ForeignKey(Disease, models.DO_NOTHING)
    treament = models.ForeignKey('Treatments', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'disease_treatment'


class Medicine(models.Model):
    name = models.CharField(max_length=255)
    adverse_reaction = models.CharField(max_length=255, blank=True, null=True)
    instruction = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'medicine'


class Symptoms(models.Model):
    id = models.IntegerField(primary_key=True)
    symptom = models.CharField(max_length=255)
    part = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'symptoms'


class Treatments(models.Model):
    treatment = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'treatments'
