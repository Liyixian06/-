import pandas as pd
import csv
import re
import os

cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
data_path = os.path.join(cur_dir, 'a39net.csv')

# 实体
diseases = []  # 疾病
symptoms = []  # 症状
departments = []  # 科室
drugs = []  # 药品

all_data = pd.read_csv(data_path, encoding='utf-8').loc[:, :].values
for data in all_data:
    # 疾病
    disease_list = str(data[0])
    diseases.append(disease_list)
    #for disease in disease_list:
        #diseases.append(disease)
    # 科室
    department_list = str(data[4]).strip().split(",")
    for department in department_list:
        departments.append(department)

    # 症状
    symptom_list = str(data[6]).replace("...", " ").strip().split(",")[:-1]
    for symptom in symptom_list:
        symptoms.append(symptom)

    # 药品
    drug_string = str(data[10]).split(",")[:-1]
    for drug in drug_string:
        drugs.append(drug)

symptoms = set(symptoms)
departments = set(departments)
drugs = set(drugs)


# 指定要保存的 CSV 文件路径
csv_file = "diseases.csv"

# 打开 CSV 文件并写入数据
with open(csv_file, "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    # 将 diseases 列表写入 CSV 文件的一列
    for disease in diseases:
        writer.writerow([disease])

csv_file = "departments.csv"

# 打开 CSV 文件并写入数据
with open(csv_file, "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    # 将 diseases 列表写入 CSV 文件的一列
    for department in departments:
        writer.writerow([department])

csv_file = "symptoms.csv"

# 打开 CSV 文件并写入数据
with open(csv_file, "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    # 将 diseases 列表写入 CSV 文件的一列
    for symptom in symptoms:
        writer.writerow([symptom])

csv_file = "drugs.csv"

# 打开 CSV 文件并写入数据
with open(csv_file, "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    # 将 diseases 列表写入 CSV 文件的一列
    for drug in drugs:
        writer.writerow([drug])

#print(diseases)



 