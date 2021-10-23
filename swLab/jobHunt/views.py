
"""
views.py
-------------------------------------------------------------------------------------------
Takes the request from urls.py and returns the corresponding views to the user on front end. View is responsible for all the operations being performed during the transfer of control from one webpage to another.
"""

from django.contrib import messages
from django.shortcuts import redirect, render
from jobHunt.models import Job,Seeker,Job_preference
from django.contrib.auth.models import auth
from django.urls import resolve

# Create your views here.
locations=["All","Hyderabad","Madhya Pradesh","Uttar Pradesh"]
titles=["Data Science","Data Analyst","Data Handling","Software Developer"]
def index(request):
    """
    Redirect the user to the index.html page that is home page of the website.
    
    :param name: request - request generated by the user.
    :param type: object of HttpRequest
    
    :return: response - index.html page
    :return type: HttpResponse
    """
   
    return render(request,"index.html",{'loc':locations,'titles':titles})
    

def search(request):
    """
    Provide the user with the list of job search result on the page search.html.
    
    :param name: request - request generated by the user.
    :param type: object of HttpRequest
    
    :return: response - search.html page
    :return type: HttpResponse
    """
    role=request.GET.get("role")
    city=request.GET.get("city")
    if(role=="" and city=="All"):
        print("here")
        res_jobs=Job.objects.all()[:10]
    elif(role=="" and city!="All"):
        res_jobs=Job.objects.filter(location=city)
    elif(city=="All"):
        res_jobs=Job.objects.filter(tag=role)
    else:
        res_jobs=Job.objects.filter(tag=role,location=city)
    jobs=[]
    for job in res_jobs:
        exp=job.experience+" years"
        jobs.append({"name":job.job_title,"company":job.company,"loc":job.location,"sal":job.salary_range,"link":job.link,"exp":exp,
        "content":job.content
        })
    print(jobs)
    return render(request,"search.html",{'jobs':jobs,'titles':titles,'loc':locations})

def login(request):
    """
    Redirect the user to the login.html page where user can give his credential to login.
    
    :param name: request - request generated by the user.
    :param type: object of HttpRequest
    
    :return: response - index.html page
    :return type: HttpResponse
    """
    if request.session['loggedin']:
        return redirect('/index')
    if request.method=="POST":
        return verify_login(request)
    return render(request,"login.html")

def verify_login(request):
    """
    Verify the credentials provided by the user and log him in if correct else redirect to the same page.
    
    :param name: request - request generated by the user.
    :param type: object of HttpRequest
    
    :return: response - index.html, login.html
    :return type: HttpResponse
    """
    email=request.POST.get("email")
    password=request.POST.get("password")
    seeker=Seeker.objects.filter(email=email,password=password)
    if seeker.exists():
        # response =redirect('/index')
        # response.set_cookie('loggedin','true')
        request.session['loggedin']=True
        request.session['email']=email
        #auth.login(request,seeker)
        return redirect('/index')
    else:
        messages.info(request, 'Invalid Credentials !!')
        print("not there")
        return render(request,'login.html')

def register(request):
    """
    Redirect the user to the register.html page where user can give his details and create a new account for the website.
    
    :param name: request - request generated by the user.
    :param type: object of HttpRequest
    
    :return: response - index.html page
    :return type: HttpResponse
    """
    location=locations[:]
    location[0]='No'
    if request.method=="POST":
        return verify_register(request)
    else:
        return render(request,"register.html",{'loc':location,'titles':titles})

def verify_register(request):
    """
    Verify if the user is a new user or existing one if new then register him log him in and redirect to the index.html else give register.html.
    
    :param name: request - request generated by the user.
    :param type: object of HttpRequest
    
    :return: response - index.html,register.html
    :return type: HttpResponse
    """
    location=locations[:]
    location[0]='No'
    email=request.POST.get("email")
    password=request.POST.get("password")
    cpassword=request.POST.get("cpassword")
    city1=request.POST.get("city1")
    city2=request.POST.get("city2")
    city3=request.POST.get("city3")
    if(city1=='No'):
        city1=None
    if(city2=='No'):
        city2=None
    if(city3=='No'):
        city3=None
    selected_titles=[]
    selected_cities=[]
    selected_titles.extend([request.POST.get("title1"),request.POST.get("title2"),request.POST.get("title3")])
    selected_titles=list(filter(lambda x: x!='',selected_titles))
    print(selected_titles,selected_cities)
    errors=[]
    if Seeker.objects.filter(email=email).exists():
        errors.append('User already Exists. Please use another email id !')
        return render(request,"register.html",{'loc':location,'titles':titles,'errors':errors})
    if password!=cpassword:
        errors.append('Passwords entered are not same !')
        return render(request,"register.html",{'loc':location,'titles':titles,'errors':errors})
    if len(selected_titles)==0:
        errors.append('Please select atleast one job preference')
        return render(request,"register.html",{'loc':location,'titles':titles,'errors':errors})
    seeker=Seeker()
    seeker.email=email
    seeker.password=password
    seeker.location1=city1
    seeker.location2=city2
    seeker.location3=city3
    s=seeker.save()
    for i in selected_titles:
        pref=Job_preference(email=seeker,job_title=i)
        pref.save()
    print(seeker)
    return redirect('/login')

    #return render(request,"index.html")

def update(request):
    """
    Redirect the user to the register.html page where user can give his details and create a new account for the website.
    
    :param name: request - request generated by the user.
    :param type: object of HttpRequest
    
    :return: response - index.html page
    :return type: HttpResponse
    """
    if not request.session['loggedin']:
        return redirect('/login')
    if request.method=="POST":
        return make_update(request)
    location=locations[:]
    location[0]="No"
    return render(request,"update.html",{'loc':location,'titles':titles})
    
def make_update(request):
    """
    Make changes made by the user in the update form.
    
    :param name: request - request generated by the user.
    :param type: object of HttpRequest
    
    :return: response - index.html page
    :return type: HttpResponse
    """
    if not request.session['loggedin']:
        return redirect('/login')
    location=locations[:]
    location[0]='No'
    email=request.POST.get("email")
    print(email)
    city1=request.POST.get("city1")
    city2=request.POST.get("city2")
    city3=request.POST.get("city3")
    if(city1=='No'):
        city1=None
    if(city2=='No'):
        city2=None
    if(city3=='No'):
        city3=None
    print(city3,city2,city1)
    selected_titles=[]
    selected_titles.extend([request.POST.get("title1"),request.POST.get("title2"),request.POST.get("title3")])
    selected_titles=list(filter(lambda x: x!='',selected_titles))
    print(selected_titles)
    errors=[]
    seeker=Seeker.objects.filter(email=email)
    if not seeker.exists():
        errors.append('User not Exists. Please enter correct email id !')
        return render(request,"update.html",{'loc':location,'titles':titles,'errors':errors})
    if len(selected_titles)==0:
        errors.append('Please select atleast one job preference')
        return render(request,"update.html",{'loc':location,'titles':titles,'errors':errors})
    seeker=seeker[0]
    seeker.location1=city1
    seeker.location2=city2
    seeker.location3=city3
    seeker.save()
    preferences=Job_preference.objects.filter(email_id=seeker)
    preferences.delete()
    for i in selected_titles:
        pref=Job_preference(email=seeker,job_title=i)
        pref.save()
    return redirect('/index')

def logout(request):
    """
    Make changes made by the user in the update form.
    
    :param name: request - request generated by the user.
    :param type: object of HttpRequest
    
    :return: response - index.html page
    :return type: HttpResponse
    """
    request.session['loggedin']=False
    return redirect('/')

