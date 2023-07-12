import os
os.environ['DJANGO_SETTINGS_MODULE']="medical.settings"

import django;django.setup()
from disease.models import Disease
from pprint import pprint

all_diseases = Disease.objects.all()
for disease in all_diseases:
    print('Name: {}, Alias: {}, Patient: {}'.format(disease.name, disease.alias, disease.patient))