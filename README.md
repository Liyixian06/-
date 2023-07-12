# week 2 小组作业

以小组为单位，完成以下任务：

从（企业）组织架构、社交网络、产品信息、明星关系等四个领域，任选一个完成。

具体要求：

1. 识别并抽取、设计该领域的实体和其间的关系，分别从：图数据库、关系型数据的角度，进行描述。

2. 使用Neo4j落地上述的设计，要求编程实现实体及相应关系的创建和编辑等操作

3. 使用MySQL落地上述的设计，要求编程实现实体及相应关系的创建和编辑等操作

4. 自行拓展实现任意功能，包括但不限于：

上述二者数据库中数据的复杂查询（多表查询、复杂关系查询）、

模拟场景应用（比如：推荐、深层关联挖掘）实现功能、

将上述前述功能封装到一个应用（如：web项目）中，整体展示、等等

  

## 数据来源

*[disease1.csv](https://github.com/Liyixian06/2023-practical-training/blob/main/neo4j/data/disease1.csv)*

  

## 环境配置

neo4j py2neo

MySQL mysqlclient

## 图数据库

### 图数据库描述

图数据库是一种专门用于处理图形数据的数据库系统。它通过使用图结构来存储和管理数据，并提供了高效的图遍历和查询能力。图数据库中的数据由节点和边组成，节点表示实体或对象，边表示节点之间的关系。图数据库的主要目标是快速查询和分析节点之间的关系，以及处理复杂的图形数据模式。它广泛应用于社交网络分析、知识图谱、推荐系统等领域。

  

图的基础：节点、关系与属性

节点：图中的对象，可带若干名-值属性，可带标签

关系：连接节点（有类型、带方向），可带若干名-值属性

  

函数create_diseases_nodes则专门用于创建疾病节点，并为每个节点设置属性。在函数中，使用Node对象创建具有相应属性的疾病节点，并通过调用graph.create将节点添加到图数据库中。

age checklist infection insurance money name period rate treatment

函数create_node用于创建一个特定标签和节点名称的节点。它接收两个参数：label表示节点的标签，nodes是一个节点名称的列表。代码使用for循环遍历nodes列表，对于每个节点名称，创建一个具有指定标签和名称的节点，并通过self.graph.create(node)将节点添加到图数据库中。

函数create_diseases_nodes用于创建疾病节点及其属性。它接收一个疾病信息的列表disease_info作为参数。代码使用for循环遍历disease_info列表中的每个疾病字典。对于每个疾病字典，根据字典中的键值对创建一个具有特定属性的疾病节点，并将节点添加到图数据库中。

函数create_graphNodes是整个过程的入口函数。它调用read_file函数来读取相关文件并获取所需的数据。然后，它依次调用create_diseases_nodes和create_node函数来创建疾病、症状、别名、部位、科室、并发症和药物等节点，并将它们添加到图数据库中。

  

函数create_relationship用于创建实体之间的关系边，首先通过将边的起始节点和结束节点连接为字符串，并将其添加到一个集合中来进行去重处理。然后，使用一个循环遍历集合中的每个边。对于每个边，它将其拆分为起始节点和结束节点，并构建一个Cypher查询语句。查询语句使用MATCH子句匹配起始节点和结束节点，然后使用CREATE子句创建起始节点与结束节点之间的关系，并指定关系类型和名称。最后，通过调用self.graph.run(query)来执行查询语句，将关系添加到图数据库中。

函数create_relationship("Disease", "Alias", rel_alias, "ALIAS_IS", "别名") 表示创建疾病节点与别名节点之间的关系，关系类型为 "ALIAS_IS"，关系名称为 "别名"，症状、部位、科室、并发症和药物之间的关系仿照其实现。

函数create_graphRels调用create_relationship函数来创建各种实体之间的关系，create_relationship函数传递以下参数：起始节点类型（start_node）、结束节点类型（end_node）、边的列表（edges）、关系类型（rel_type）和关系名称（rel_name）。

  

### 图数据库编辑

- 查
    
    ```Python
    def get_disease(self, disease_name):
        """
        获取疾病节点
        :param disease_name: str, 疾病名称
        :return: Node, 疾病节点
        """
        query = f"MATCH (d:Disease) WHERE d.name = '{disease_name}' RETURN d"
        result = self.graph.run(query).data()
        if result:
            return result[0]['d']
        return None
            
    def disease_drugs_symptoms(self, disease_name):
       """
       查询与给定疾病相关的所有药品和症状
       :param disease_name: str, 疾病名称
       :return: 查询结果
       """
       query = f"MATCH (d:Disease)-[:HAS_DRUG]->(dr:Drug), (d:Disease)-[:HAS_SYMPTOM]->(s:Symptom) WHERE d.name = '{disease_name}' RETURN dr, s"
       return self.graph.run(query).data()
    ```
    
- 增
    
    ```Python
    def update_disease(self, disease_name, new_info):
            """
            更新疾病节点属性
            :param disease_name: str, 疾病名称
            :param new_info: Dict, 新的疾病属性
            :return: Node, 更新后的疾病节点
            """
            node = self.get_disease(disease_name)
            if node:
                for key, value in new_info.items():
                    if value.strip():
                        node[key] = value
                self.graph.push(node)
                return node
            return None
    ```
    
- 删
    
    ```Python
      def delete_disease(self, disease_name):
            """
            删除疾病节点
            :param disease_name: str, 疾病名称
            :return: bool, 表示是否成功删除节点
            """
            node = self.get_disease(disease_name)
            if node:
                self.graph.delete(node)
                return True
            return False
    ```
    
- 改
    
    ```Python
    updated_node = handler.update_disease(name, updated_info)
    if updated_node:
        print("Disease updated:")
        encoded_updated_node = {k: v.encode('utf-8').decode('utf-8') if isinstance(v, str) else v for k, v in
                                updated_node.items()}
        print(encoded_updated_node)
    else:
        print("Disease not found.")
    ```
    

## 关系型数据库

### 关系型数据库描述

关系型数据库是一种以关系模型为基础的数据库系统。它使用表格（关系）来组织和表示数据，并使用结构化查询语言（SQL）进行数据管理和查询。关系型数据库的核心思想是将数据分解为多个表格，每个表格包含行和列，其中行表示记录，列表示属性。关系型数据库通过定义表之间的关系（主键、外键等）来建立数据之间的联系。它具有事务处理能力和数据一致性保证，适用于大规模数据存储和复杂的数据操作需求。

  

MySQL设计

- 疾病表：id、疾病名、又名、患病人群、传染性、是否在医保范围
    
- 症状表：id、部位、症状
    
- 药物表：id、药物名、副作用、服用指导、费用
    
- 治疗表：id、名字（手术、心理、饮食、物理……）
    
- 科室表：id、科室名
    
- 疾病和症状（多对多）
    
- 疾病和药物（多对多）
    
- 疾病和治疗（多对多）
    
- 疾病和科室（多对多）
    

  

### 关系型数据库编辑
