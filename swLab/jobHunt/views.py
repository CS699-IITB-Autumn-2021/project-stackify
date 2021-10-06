from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,"index.html")

def search(request):
    return render(request,"search.html")

def login(request):
    return render(request,"login.html")

def register(request):
    return render(request,"register.html")

def update(request):
    return render(request,"update.html")

