from django.db import models
from django.db.models.deletion import CASCADE
from datetime import date, datetime

# Create your models here.

class Seeker(models.Model):
    email=models.CharField(max_length=100)
    location1=models.CharField(max_length=100)
    location2=models.CharField(max_length=100)
    location2=models.CharField(max_length=100)

class Job_preference(models.Model):
    email=models.ForeignKey(Seeker,on_delete=models.CASCADE)
    job_title=models.CharField(max_length=30)

class Job(models.Model):
    job_title=models.CharField(max_length=30)
    tag=models.CharField(max_length=50)
    company=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    salary_range=models.CharField(max_length=50)
    link=models.CharField(max_length=200)
    experience=models.CharField(max_length=30)
    content=models.CharField(max_length=200)
    date=models.DateField(blank=True,default=date.today)
