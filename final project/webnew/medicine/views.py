from django.shortcuts import render
from medicine.searchqa.question_match import *
from medicine.searchqa.question_cypher import *
from medicine.searchqa.question_answer import *
from py2neo import *
list_Q=[]
list_A=[]
lasttext=""
match = Question_Match()
Cypher = Question_to_Cypher()
answer = Question_Answer()
g = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))
def index(request):
    return render(request,'medicine/index.html')
def graph(request):
    return render(request,'medicine/graph.html')
def departsearch(request):
    depart = []
    departs = list(NodeMatcher(graph=g).match("Department"))
    for d in departs:
        depart.append(d['name'])

    if request.method == 'POST':
        sign = 1
        dtext = request.POST.get("dd","")
        nametext = request.POST.get("textd","")
        global lasttext
        lasttext = nametext if nametext else lasttext
        cypher = "MATCH (n)-[r:DEPARTMENT_IS]->(m:Department) where m.name='"+lasttext+"' return n "
        if dtext:
            cypher = "MATCH (n:Disease)-[r:DEPARTMENT_IS]->(m:Department) where m.name='" + lasttext + "' and n.name contains '"+dtext+"' return n "
        result = g.run(cypher).data()
        disease = []
        altername = []
        inspect = []
        introduction = []
        population = []
        treatment = []
        count = 0
        for r in result:
            rs = r["n"]
            disease.append(rs["name"])
            altername.append(rs["altername"])
            inspect.append(rs["inspect"])
            introduction.append(rs["introduction"])
            population.append(rs["population"])
            treatment.append(rs["treatment"])
            count += 1
        info = zip(disease,altername,inspect,introduction,population,treatment)
        context = {"info": info, "sign":sign,"depart":depart}

        return render(request,'medicine/departsearch.html',context=context)
    else:

        sign = ""

        return render(request,'medicine/departsearch.html',context={"depart":depart,"sign":sign})



def search(request):
    if request.method == 'POST':
        ybtn = request.POST.get('ybtn','')
        if ybtn!='':

            search_text = request.POST.get('searchtext','')
            question = search_text
            ans = QA(question,match,Cypher,answer)
            if(len(list_A)>4):
                del(list_A[0])
                del(list_Q[0])
            list_A.append(ans)
            list_Q.append(question)
            ziped = zip(list_A,list_Q)
            return render(request,'medicine/search.html',context={"ziped":ziped})

    else :
        list_A.clear()
        list_Q.clear()
    return render(request, 'medicine/search.html')
# Create your views here.
