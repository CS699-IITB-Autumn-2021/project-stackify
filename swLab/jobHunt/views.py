from django.shortcuts import render
from django.http import HttpResponse
from jobHunt.models import Job
# Create your views here.
def index(request):
    return render(request,"index.html")

def search(request):
    role=request.GET.get("role")
    city=request.GET.get("city")
    print(role,city)
    res_jobs=Job.objects.filter(tag=role,location=city)
    jobs=[]
    for job in res_jobs:
        if int(job.experience)<2:
            exp=job.experience+" year"
        else:
            exp=job.experience+" years"
        jobs.append({"name":job.job_title,"company":job.company,"loc":job.location,"sal":job.salary_range,"link":job.link,"exp":exp,
        "content":job.content
        })
    print(jobs)
    return render(request,"search.html",{'jobs':jobs})

def login(request):
    return render(request,"login.html")

def register(request):
    return render(request,"register.html")

def update(request):
    return render(request,"update.html")

