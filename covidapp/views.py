from django.shortcuts import render

def home(request):
    return render(request,'index.html')
def finder(request):
    return render(request,'finder.html')
def signup(request):
    return render(request,'signup.html')

def fallback(request):
    return render(request,'fallback.html')


#survey functions

def takesurvey(request):
    return render(request,'survey.html')



# tracker functions and data
def trackerna(request):
    return render(request,'trackerna.html')

#end tracker

