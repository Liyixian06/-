class Question_to_Cypher:
    def transfer(self, question_data):
        # 将提取的实体分类
        if not question_data:
            return []
        word_dict = question_data['word_dict']
        disease_list = []
        symptom_list = []
        drug_list = []
        for entity, type in word_dict.items():
            if type == 'disease':
                disease_list.append(entity)
            elif type == 'symptom':
                symptom_list.append(entity)
            elif type == 'drug':
                drug_list.append(entity)
        question_types = question_data['question_types']
        cyphers = []
        for question_type in question_types:
            cypher = {}
            match = []
            cypher['question_type'] = question_type
            if question_type == 'disease_intro' or question_type == 'disease_dept' \
                    or question_type == 'disease_cause' or question_type == 'disease_symptom' \
                    or question_type == 'disease_check' or question_type == 'disease_drug' \
                    or question_type == 'disease_treat' or question_type == 'disease_complication':
                match = self.match_cypher(disease_list, question_type)

            elif question_type == 'symptom_disease':
                match = self.match_cypher(symptom_list, question_type)

            elif question_type == 'drug_disease':
                match = self.match_cypher(drug_list, question_type)

            elif question_type == 'disease_others' or question_type == 'symptom_others' or question_type == 'drug_others' \
                    or question_type == 'no match entity':
                match = ["no match cypher"]

            if match:
                cypher['match'] = match
                cyphers.append(cypher)

        return cyphers

    def match_cypher(self, entity_list, question_type):
        if not entity_list:
            return []
        match = []

        # 简介
        if question_type == 'disease_intro':
            match = ["MATCH (n:Disease) where n.name = '{}' return n.name, n.introduction".format(i) for i in
                     entity_list]
        # 科室（关系）
        elif question_type == 'disease_dept':
            match = [
                "MATCH (n:Disease)-[r:DEPARTMENT_IS]-(m:Department) where n.name = '{}' return n.name, m.name".format(i)
                for i in entity_list]
        # 病因
        # elif question_type == 'disease_cause':
        # match = ["MATCH (n:Disease) where n.name = '{}' return n.name, n.cause".format(i) for i in entity_list]
        # 症状（关系）
        elif question_type == 'disease_symptom':
            match = ["MATCH (n:Disease)-[r:HAS_SYMPTOM]-(m:Symptom) where n.name = '{}' return n.name, m.name".format(i)
                     for i in entity_list]
        # 检查
        elif question_type == 'disease_check':
            match = ["MATCH (n:Disease) where n.name = '{}' return n.name, n.inspect".format(i) for i in entity_list]
        # 药物（关系）
        elif question_type == 'disease_drug':
            match = ["MATCH (n:Disease)-[r:HAS_DRUG]-(m:Drug) where n.name = '{}' return n.name, m.name".format(i) for i
                     in entity_list]
        # 治疗方法
        elif question_type == 'disease_treat':
            match = ["MATCH (n:Disease) where n.name = '{}' return n.name, n.treatment".format(i) for i in entity_list]
        # 并发症（关系）
        elif question_type == 'disease_complication':
            match_1 = [
                "MATCH (n:Disease)-[r:HAS_COMPLICATION]-(m:Disease) where n.name = '{}' return n.name, m.name".format(i)
                for i in entity_list]
            match_2 = [
                "MATCH (m:Disease)-[r:HAS_COMPLICATION]-(n:Disease) where n.name = '{}' return n.name, m.name".format(i)
                for i in entity_list]
            match = match_1 + match_2
        # 已知症状查疾病
        elif question_type == 'symptom_disease':
            match = [
                "MATCH (n:Disease)-[r:HAS_SYMPTOM]-(m:Symptom) where m.name = '{}' return n.name, m.name limit 25".format(
                    i) for i in entity_list]
        # 已知药品查疾病
        elif question_type == 'drug_disease':
            match = [
                "MATCH (n:Disease)-[r:HAS_DRUG]-(m:Drug) where m.name = '{}' return n.name, m.name limit 25".format(i)
                for i in entity_list]

        return match