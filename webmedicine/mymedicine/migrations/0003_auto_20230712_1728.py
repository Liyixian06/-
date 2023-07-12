# Generated by Django 3.2.20 on 2023-07-12 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymedicine', '0002_auto_20230712_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseasedepartment',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymedicine.department'),
        ),
        migrations.AlterField(
            model_name='diseasedepartment',
            name='disease',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymedicine.disease'),
        ),
        migrations.AlterField(
            model_name='diseasemedicine',
            name='disease',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymedicine.disease'),
        ),
        migrations.AlterField(
            model_name='diseasemedicine',
            name='medicine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymedicine.medicine'),
        ),
        migrations.AlterField(
            model_name='diseasesymptom',
            name='disease',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymedicine.disease'),
        ),
        migrations.AlterField(
            model_name='diseasesymptom',
            name='symptom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymedicine.symptoms'),
        ),
        migrations.AlterField(
            model_name='diseasetreatment',
            name='disease',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymedicine.disease'),
        ),
        migrations.AlterField(
            model_name='diseasetreatment',
            name='treament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymedicine.treatments'),
        ),
    ]
