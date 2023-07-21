import csv

import pickle

from medicine.searchqa.question_cypher import *
from medicine.searchqa.question_answer import *
import os
import ahocorasick
import csv
import jieba
import jieba.posseg as pseg

jieba.load_userdict("C:/Users/DELL/Desktop/question_ver2.0/worddict.txt")

from sentence_transformers import SentenceTransformer
import scipy
import re



class Question_Match:
    def __init__(self):
        # 疑问词
        self.intro_queswords = ['简介', '什么是', '是什么', '是啥', '介绍', '描述']
        self.dept_queswords = ['属于', '什么科', '科室', '哪个科', '哪科']
        self.cause_queswords = ['为什么', '原因', '病因', '怎么会', '导致', '造成', '为啥', '为何', '成因', '怎么就',
                                '为什么会']
        self.symptom_queswords = ['症状', '表现', '症候', '现象', '表征']
        self.check_queswords = ['检查', '项目', '查出', '查出来', '怎么查', '测出']
        self.drug_queswords = ['药', '什么药', '用药', '药品', '啥药']
        self.treat_queswords = ['怎么治', '方法', '办法', '治疗', '疗法', '咋治', '医治', '怎么医', '怎么办']
        self.cmp_queswords = ['并发症', '并发', '一起发生', '伴随', '一起出现']
        self.disease_queswords = ['怎么办', '咋办', '什么病', '啥病', '怎么回事', '哪种病', '哪种疾病', '什么疾病']
        self.cure_queswords = ['治什么', '治疗什么', '治啥', '治疗', '有什么用', '做什么', '干什么', '干啥', '用来',
                               '用', '要']
        self.all_disease_queswords = self.intro_queswords + self.dept_queswords + self.cause_queswords + self.symptom_queswords \
                                     + self.check_queswords + self.drug_queswords + self.treat_queswords + self.cmp_queswords
        # 读入实体
        self.disease_list = []
        self.symptom_list = []
        self.drug_list = []
#edicine/searchqa/
        with open('medicine/searchqa/data/diseases.csv', mode='r', encoding='utf8', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.disease_list.append(row[0])
        with open('medicine/searchqa/data/symptoms.csv', mode='r', encoding='utf8', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.symptom_list.append(row[0])
        with open('medicine/searchqa/data/drugs.csv', mode='r', encoding='utf8', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.drug_list.append(row[0])
        f.close()
        self.wordlist = self.disease_list + self.symptom_list + self.drug_list
        # 构建实体对应类型的字典
        self.worddict = dict()
        for word in self.disease_list:
            self.worddict[word] = 'disease'
        for word in self.symptom_list:
            self.worddict[word] = 'symptom'
        for word in self.drug_list:
            self.worddict[word] = 'drug'
        # 构建 AC 自动机
        self.actree = ahocorasick.Automaton()
        for index, word in enumerate(self.wordlist):
            self.actree.add_word(word, (index, word))
        self.actree.make_automaton()
        # 构建语义相似度模型
        self.model = SentenceTransformer('distiluse-base-multilingual-cased')
        # self.model = SentenceTransformer('./model')
        # self.model.save("./model")
         self.wordlist_embeddings = self.model.encode(self.wordlist)
        # pickle.dump(self.wordlist_embeddings,open("encode.pkl","wb"))
        # self.wordlist_embeddings = pickle.load(open('encode.pkl', 'rb'))


    # 从问句中提取实体
    def extract_words(self, question):
        ques_word_list = []
        for i in self.actree.iter(question):
            ques_word_list.append(i[1][1])
        # 在匹配出的实体中，如果有短的词存在长的词中，去掉短的词
        short_words = []
        for i1 in ques_word_list:
            for i2 in ques_word_list:
                if i1 in i2 and i1 != i2:
                    short_words.append(i1)
        final_ques_word_list = [i for i in ques_word_list if i not in short_words]
        ques_word_dict = {i: self.worddict.get(i) for i in final_ques_word_list}
        return ques_word_dict

    # 检查某类问题的疑问词是否出现在了问句里
    def ques_type(self, queswords, question):
        for word in queswords:
            if word in question:
                return True
        return False

    def match(self, question):
        question_data = {}
        ques_word_dict = self.extract_words(question)
        question_data['word_dict'] = ques_word_dict
        question_types = []
        no_entity = ""
        # 如果没有检索到任何实体，开始相似度查询
        if not ques_word_dict:
            queries = []
            words = pseg.cut(question)
            for word, flag in words:
                if (flag == 'x' or flag == 'n') and len(word) > 1:
                    queries.append(word)
            # print(queries)
            no_entity ="没有精准查询到您输入的内容，请确保输入了正确的专有名词。"

            number_top_matches = 5
            query_embeddings = self.model.encode(queries)
            for query, query_embedding in zip(queries, query_embeddings):
                no_entity +="您想要查询的是否是："+ query
                # 搜索是否有名字包含输入内容的实体
                similar_word_list = []
                for item in self.wordlist:
                    if re.match('.*' + query + '.*', item):
                        similar_word_list.append(item)
                no_entity += "- 数据库中包含您输入内容的 {} 个词如下：".format(len(similar_word_list))
                no_entity += '，'.join(str(i) for i in similar_word_list)
                # 搜索和输入内容最相似的实体
                distances = scipy.spatial.distance.cdist([query_embedding], self.wordlist_embeddings, 'cosine')[0]
                results = zip(range(len(distances)), distances)
                results = sorted(results, key=lambda x: x[1])
                no_entity+="- 和您输入最相似的 {} 个词及匹配度如下：".format(number_top_matches)
                for idx, distance in results[0:number_top_matches]:
                    no_entity+=self.wordlist[idx].strip()+"(%.4f)" % (1 - distance)

            if queries:
                question_types.append('no match entity')
            else:
                return {},no_entity
        # 问句中包含哪些类型的实体
        entity_types = []
        for type in ques_word_dict.values():
            entity_types.append(type)

        # 匹配问题类型
        # 单个疾病的信息查询
        # 简介
        if self.ques_type(self.intro_queswords, question) and ('disease' in entity_types):
            question_types.append('disease_intro')
        # 科室
        if self.ques_type(self.dept_queswords, question) and ('disease' in entity_types):
            question_types.append('disease_dept')
        # 病因
        if self.ques_type(self.cause_queswords, question) and ('disease' in entity_types):
            question_types.append('disease_cause')
        # 症状
        if self.ques_type(self.symptom_queswords, question) and ('disease' in entity_types):
            question_types.append('disease_symptom')
        # 检查
        if self.ques_type(self.check_queswords, question) and ('disease' in entity_types):
            question_types.append('disease_check')
        # 药物
        if self.ques_type(self.drug_queswords, question) and ('disease' in entity_types):
            question_types.append('disease_drug')
        # 治疗方法
        if self.ques_type(self.treat_queswords, question) and ('disease' in entity_types):
            question_types.append('disease_treat')
        # 并发症
        if self.ques_type(self.cmp_queswords, question) and ('disease' in entity_types):
            question_types.append('disease_complication')

        # 通过症状推测疾病
        if (self.ques_type(self.disease_queswords, question) or self.ques_type(self.symptom_queswords,
                                                                               question) or self.ques_type(
                self.cause_queswords, question) or self.ques_type(self.treat_queswords, question)) and (
                'symptom' in entity_types):
            question_types.append('symptom_disease')
        # 药品能治疗的疾病
        if self.ques_type(self.cure_queswords, question) and ('drug' in entity_types):
            question_types.append('drug_disease')

        if ('disease' in entity_types) and self.ques_type(self.all_disease_queswords, question) == False:
            question_types.append('disease_others')
        if ('drug' in entity_types) and self.ques_type(self.cure_queswords, question) == False:
            question_types.append('drug_others')
        if ('symptom' in entity_types) and (
                self.ques_type(self.disease_queswords, question) or self.ques_type(self.symptom_queswords,
                                                                                   question) or self.ques_type(
                self.cause_queswords, question)) == False:
            question_types.append('symptom_others')

        question_data['question_types'] = question_types
        return question_data,no_entity

def QA(question,match,Cypher,answer):
    question_data,no_entity = match.match(question)
        # print(question_data)
    cyphers = Cypher.transfer(question_data)
        # print(cyphers)
    anss = answer.match_answer(cyphers)
    ans =""
    for a in anss:
        ans+=a
    if no_entity and no_entity !="没有精准查询到您输入的内容，请确保输入了正确的专有名词。":
        ans = no_entity

    return ans



