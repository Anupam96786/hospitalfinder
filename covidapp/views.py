from django.shortcuts import render
from django.http import HttpResponse
#imports for tracker functions
from io import BytesIO
import base64
import matplotlib
matplotlib.use("Agg")
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
# Create your views here.

def home(request):
    return render(request,'index.html')
def finder(request):
    return render(request,'finder.html')
def signup(request):
    return render(request,'signup.html')




#survey functions

def takesurvey(request):
    return render(request,'survey.html')


def surveysubmit(request):
    context={}
    result=''
    #symptoms
    allsym=[request.POST['anosmia'],request.POST['throat'],request.POST['congestion'],request.POST['runny'],request.POST['headache'],request.POST['loa'],request.POST['abdomen'],request.POST['cough'],request.POST['fatigue'],request.POST['dihorrea']]
    anosmia=request.POST['anosmia']
    dyspnea=request.POST['dyspnea']
    fever=request.POST['fever']
    #dihorrea=request.POST['dihorrea']
    #fatigue=request.POST['fatigue']
    #cough=request.POST['cough']
    #abdomen=request.POST['abdomen']
    #loa=request.POST['loa']
    #headache=request.POST['headache']
    #runny=request.POST['runny']
    #congestion=request.POST['congestion']
    #throat=request.POST['throat']
    contact=request.POST['contact']
    #risks
    risk=0
    allrisk=[request.POST['age'],request.POST['aids'],request.POST['kidney'],request.POST['liver'],request.POST['lung'],request.POST['heart'],request.POST['highbp'],request.POST['diabetes']]
    #age=request.POST['age']
    #diabetes=request.POST['diabetes']
    #highbp=request.POST['highbp']
    #heart=request.POST['heart']
    #lung=request.POST['lung']
    #liver=request.POST['liver']
    #kidney=request.POST['kidney']
    #aids=request.POST['aids']
    if(allrisk.count('1')>=1):
        risk=1
    context['risk']=risk
    if dyspnea=='1':
        return render(request,'case2severe.html',context)
    elif(anosmia=='1' or fever=='1'):
        if(allsym.count('1')>=1):
            return render(request,'case2severe.html',context)
        else:
            return render(request,'case2.html',context)
    else:
        return render(request,'case1.html',context)


#end survey

# tracker functions and data
def trackerna(request):
    return render(request,'trackerna.html')

def bar(state_data):
    n_groups = 33
    state = np.array(list(str(i[1]) for i in state_data))
    infected = np.array(list(int(i[2]) for i in state_data))
    cured = np.array(list(int(i[3]) for i in state_data))
    death = np.array(list(int(i[4]) for i in state_data))
    r_infected = infected - cured - death
    r_cured = r_infected + cured
    r_death = infected
    i=r_infected.sum()
    d=death.sum()
    c=cured.sum()
    plt.style.use('seaborn')
    index = np.arange(n_groups)
    plt.barh(index, r_death, align='center',
             color="#E10000",
             label="DEATH")
    plt.barh(index, r_cured, align="center",
             color="#18E324",
             label="CURED")
    plt.barh(index, r_infected, align="center",
             color="#003EBA",
             label="ACTIVE")
    plt.yticks(index, state, fontsize=7)
    plt.xlim(0, max(infected+500))
    plt.xlabel('Number of Cases')
    plt.title('Corona Virus Cases')
    plt.legend()
    buf = BytesIO()
    plt.savefig(buf,format='png', bbox_inches="tight", dpi=300)
    plt.clf()
    piegraph=pie(i,d,c)
    bargraph = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return bargraph,piegraph

def pie(i,d,c):
    activities = ['ACTIVE', 'DEATH', 'CURED']
    slices = [i,d,c]
    colors = ['#003EBA', '#E10000','#18E324']
    plt.pie(slices, labels = activities, colors=colors,
        startangle=90, shadow = True, explode = (0.1, 0.1, 0.1),
        radius = 0.89, autopct = '%1.2f%%')
    plt.legend()
    buf = BytesIO()
    plt.savefig(buf,format='png', bbox_inches="tight", dpi=300)
    plt.close()
    piegraph = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return piegraph

def datacollect():
    raw_data = requests.get("https://www.mohfw.gov.in/").text
    soup = BeautifulSoup(raw_data, "html.parser")
    l1 = []
    for tr in soup.find_all("tbody")[0].find_all("tr"):
        d1 = tr.get_text().split("\n")
        l2 = []
        for i in d1:
            if i != "":
                l2.append(i)
        l1.append(l2)
    indiadata = l1[33]
    l1 = l1[0:33]
    bargraph,piegraph=bar(l1)
    return l1,indiadata,bargraph,piegraph

#statedata,indiadata,bargraph,piegraph=datacollect()

def tracker(request):
    context={}
    context['statedata']=statedata
    context['indiadata']=indiadata
    context['bar']=bargraph
    context['pi']=piegraph
    return render(request,'tracker.html',context)

#end tracker

