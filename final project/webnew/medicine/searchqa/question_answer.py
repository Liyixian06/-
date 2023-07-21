from py2neo import Graph, NodeMatcher


class Question_Answer:
    def __init__(self):
        self.graph = Graph(
            "bolt: // localhost:7687",
            auth=("neo4j", "12345678")
        )
        # self.matcher = NodeMatcher(graph)

    def match_answer(self, cyphers):
        output_answer = []
        if not cyphers:
            output_answer = '''没有理解您输入的问题。您可以询问疾病的介绍、症状、治疗方法、并发症，以及药物的用途等信息。以下是一些供参考的问法：
            - 最近总是咳嗽、打喷嚏，怎么办？
            - 小儿癫痫是什么病，怎么治？
            - 家里有一盒金莲花胶囊，这是干什么用的？'''
        for cypher in cyphers:
            question_type = cypher['question_type']
            match = cypher['match']
            answer = []
            for query in match:
                if query != "no match cypher":
                    cursors = self.graph.run(query).data()
                    answer += (cursors)
            output_answer.append(self.form_answer(question_type, answer))
        return output_answer

    def form_answer(self, question_type, answer):
        output_answer = []
        if not answer and question_type != 'disease_others' and question_type != 'symptom_others' and question_type != 'drug_others':
            return ''
        # 简介
        if question_type == 'disease_intro':
            form = [i['n.introduction'] for i in answer if i['n.introduction'] != None]
            disease = answer[0]['n.name']
            output_answer = '{0}的简介如下：{1}'.format(disease, '；'.join(
                list(set(form)))) if form != [] else '没有查询到{0}的简介，请尝试其他问题。'.format(disease)

        # 科室（关系）
        elif question_type == 'disease_dept':
            form = [i['m.name'] for i in answer]
            disease = answer[0]['n.name']
            output_answer = '{0}隶属的科室是：{1}'.format(disease, '；'.join(
                list(set(form)))) if form != [] else '没有查询到{0}隶属的科室，请尝试其他问题。'.format(disease)

        # 病因
        elif question_type == 'disease_cause':
            form = [i['n.cause'] for i in answer if i['n.cause'] != None]
            disease = answer[0]['n.name']
            output_answer = '{0}可能的病因有：{1}'.format(disease, '；'.join(
                list(set(form)))) if form != [] else '没有查询到{0}可能的病因，请尝试其他问题。'.format(disease)

        # 症状（关系）
        elif question_type == 'disease_symptom':
            form = [i['m.name'] for i in answer]
            disease = answer[0]['n.name']
            output_answer = '{0}的症状有：{1}'.format(disease, '；'.join(
                list(set(form)))) if form != [] else '没有查询到{0}的症状，请尝试其他问题。'.format(disease)

        # 检查
        elif question_type == 'disease_check':
            form = [i['n.inspect'] for i in answer if i['n.inspect'] != None]
            disease = answer[0]['n.name']
            output_answer = '检查{0}要做的项目有：{1}'.format(disease, '；'.join(
                list(set(form)))) if form != [] else '没有查询到{0}的相关检查项目，请尝试其他问题。'.format(disease)

        # 药物（关系）
        elif question_type == 'disease_drug':
            form = [i['m.name'] for i in answer]
            disease = answer[0]['n.name']
            output_answer = '治疗{0}的药物有：{1}'.format(disease, '；'.join(
                list(set(form)))) if form != [] else '没有查询到能治疗{0}的药物，请尝试其他问题。'.format(disease)

        # 治疗方法
        elif question_type == 'disease_treat':
            form = [i['n.treatment'] for i in answer if i['n.treatment'] != None]
            disease = answer[0]['n.name']
            output_answer = '{0}的治疗方法有：{1}'.format(disease, '；'.join(
                list(set(form)))) if form != [] else '没有查询到{0}的治疗方法，请尝试其他问题。'.format(disease)

        # 并发症（关系）
        elif question_type == 'disease_complication':
            form = [i['m.name'] for i in answer]
            disease = answer[0]['n.name']
            output_answer = '{0}的并发症有：{1}'.format(disease, '；'.join(
                list(set(form)))) if form != [] else '没有查询到{0}的并发症，请尝试其他问题。'.format(disease)

        # 已知症状查疾病（关系）
        elif question_type == 'symptom_disease':
            form = [i['n.name'] for i in answer]
            symptom = answer[0]['m.name']
            output_answer = '{0}的症状可能是因为如下疾病：{1}。关于治疗方式，请进一步查询。'.format(symptom, '；'.join(list(set(form)))) if form != [] else '没有查询到{0}可能对应的疾病，请尝试其他问题。'.format(symptom)

        # 已知药品查疾病（关系）
        elif question_type == 'drug_disease':
            form = [i['n.name'] for i in answer]
            drug = answer[0]['m.name']
            output_answer = '{0}可以治疗的疾病有：{1}'.format(drug, '；'.join(list(set(form)))) if form != [] else '没有查询到{0}可以治疗的疾病，请尝试其他问题。'.format(drug)

        elif question_type == 'disease_others':
            output_answer = '没有查询到该疾病的相关信息。您是否想问：疾病的简介/所属科室/病因/症状/检查项目/药物/治疗方法/并发症？'
        elif question_type == 'symptom_others':
            output_answer = '没有查询到该症状的相关信息。您是否想问：该症状可能属于哪种疾病？'
        elif question_type == 'drug_others':
            output_answer = '没有查询到该药物的相关信息。您是否想问：该药物可以治疗哪些疾病？'

        return output_answer