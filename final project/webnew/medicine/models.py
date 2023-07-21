from py2neo import Graph, Node, Relationship
import pandas as pd
import re
import os


class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'a39net.csv')
        self.graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))

    def clean_node(self):
        # 清空数据库
        query = "MATCH (n) DETACH DELETE n"
        self.graph.run(query)

    def read_file(self):
        """
        读取文件，获得实体，实体关系
        :return:
        """
        # 实体
        diseases = []  # 疾病
        symptoms = []  # 症状
        parts = []  # 部位
        departments = []  # 科室
        complications = []  # 并发症
        drugs = []  # 药品

        diseases_infos = []
        # 关系
        disease_to_symptom = []  # 疾病与症状关系
        diseases_to_part = []  # 疾病与部位关系
        disease_to_department = []  # 疾病与科室关系
        disease_to_complication = []  # 疾病与并发症关系
        disease_to_drug = []  # 疾病与药品关系

        all_data = pd.read_csv(self.data_path, encoding='utf-8').loc[:, :].values
        for data in all_data:
            disease_dict = {}  # 疾病信息
            # 疾病
            disease = str(data[0]).replace("...", " ").strip()
            disease_dict["name"] = disease
            diseases.append(disease)
            # 简介
            introduction = str(data[1]).strip()
            disease_dict["introduction"] = introduction
            # 别名
            altername = str(data[2]).strip()
            disease_dict["altername"] = altername
            # 部位
            part_list = str(data[3]).strip().split() if str(data[3] != None) else "未知"
            for part in part_list:
                parts.append(part)
                diseases_to_part.append([disease, part])
            # 科室
            department_list = str(data[4]).strip().split(",")
            for department in department_list:
                departments.append(department)
                disease_to_department.append([disease, department])
            # 易感人群
            population = str(data[5]).strip()
            disease_dict["population"] = population
            # 症状
            symptom_list = str(data[6]).replace("...", " ").strip().split(",")[:-1] if str(data[6]) else "未知"
            for symptom in symptom_list:
                symptoms.append(symptom)
                disease_to_symptom.append([disease, symptom])
            # 检查项
            inspect = str(data[7]).strip()
            disease_dict["inspect"] = inspect
            # 并发症
            complication_list = str(data[8]).strip().split(",")[:-1] if str(data[8]) else "未知"
            for complication in complication_list:
                complications.append(complication)
                disease_to_complication.append([disease, complication])
            # 治疗方法
            treat = str(data[9]).strip()
            disease_dict["treatment"] = treat
            # 药品
            drug_string = str(data[10]).split(",")[:-1]
            for drug in drug_string:
                drugs.append(drug)
                disease_to_drug.append([disease, drug])

            diseases_infos.append(disease_dict)

        return set(diseases), set(symptoms), set(parts), set(departments), set(complications), \
            set(drugs), disease_to_symptom, diseases_to_part, disease_to_department, \
            disease_to_complication, disease_to_drug, diseases_infos

    def create_node(self, label, nodes):
        """
        创建节点
        :param label: 标签
        :param nodes: 节点
        :return:
        """
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.graph.create(node)
        return

    def create_one_node(self, label, node_name):
        """
        创建节点
        :param label: 标签
        :param nodes: 节点
        :return:
        """
        node = Node(label, name=node_name)
        self.graph.create(node)
        return

    def create_diseases_nodes(self, disease_info):
        """
        创建疾病节点的属性
        :param disease_info: list(Dict)
        :return:
        """
        count = 0
        for disease_dict in disease_info:
            node = Node("Disease", name=disease_dict['name'], introduction=disease_dict['introduction'],
                        altername=disease_dict['altername'], population=disease_dict['population'],
                        inspect=disease_dict['inspect'], treatment=disease_dict['treatment'], )
            self.graph.create(node)
            count += 1
            print(count)  # debug用
        return

    def create_graphNodes(self):
        """
        创建知识图谱实体
        :return:
        """
        disease, symptom, part, department, complication, drug, rel_symptom, rel_part, \
            rel_department, rel_complication, rel_drug, rel_infos = self.read_file()
        self.create_diseases_nodes(rel_infos)
        self.create_node("Symptom", symptom)
        self.create_node("Part", part)
        self.create_node("Department", department)
        for complication_one in complication:
            if complication_one not in disease:
                self.create_one_node("Disease", complication_one)
        self.create_node("Drug", drug)

        return

    def create_graphRels(self):
        disease, symptom, part, department, complication, drug, rel_symptom, rel_part, \
            rel_department, rel_complication, rel_drug, rel_infos = self.read_file()

        self.create_relationship("Disease", "Symptom", rel_symptom, "HAS_SYMPTOM", "症状")
        self.create_relationship("Disease", "Part", rel_part, "PART_IS", "发病部位")
        self.create_relationship("Disease", "Department", rel_department, "DEPARTMENT_IS", "所属科室")
        self.create_relationship("Disease", "Disease", rel_complication, "HAS_COMPLICATION", "并发症")
        self.create_relationship("Disease", "Drug", rel_drug, "HAS_DRUG", "药品")

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        """
        创建实体关系边
        :param start_node:
        :param end_node:
        :param edges:
        :param rel_type:
        :param rel_name:
        :return:
        """
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.graph.run(query)
                count += 1
                # print(rel_type, count, all)
            except Exception as e:
                print(e)
        return


# 主函数
if __name__ == "__main__":
    handler = MedicalGraph()
    handler.clean_node()
    handler.create_graphNodes()
    handler.create_graphRels()