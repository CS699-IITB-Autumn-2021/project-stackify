"""
models.py
-------------------------------------------------------------------
This contains all the db tables in the form of class to create a table instance we can just call this class's object and add remove or update the database.
"""
from django.db import models
from django.db.models.deletion import CASCADE
from datetime import date, datetime

# Create your models here.

class Seeker(models.Model):
    """
    class Seeker: Stores infromation about the registered user and their location preference.
    :param name: email - Email id of the user is the primary key for Seeker table
    :param type: string
    :param name: location1 - first location preference
    :param type: string
    :param name: location2 - second location prefernce
    :param type: string
    :param name: location3 - third location preference
    :param type: string
    """
    email=models.CharField(max_length=100)
    location1=models.CharField(max_length=100)
    location2=models.CharField(max_length=100)
    location2=models.CharField(max_length=100)

class Job_preference(models.Model):
    """
    class Job_preference: Strores the mapping of job preference of user with user mail id.
    :param name: email - foreign key to email in Seeker table.
    :param type: string
    :param name: job_title - job preference of the user
    :param type: string 
    """
    email=models.ForeignKey(Seeker,on_delete=models.CASCADE)
    job_title=models.CharField(max_length=30)

class Job(models.Model):
    """
    class Job: Stores the jobs data crapped from job portals.
    :param name: job_title - used to identify the job category locally
    :param type: string
    :param name: tag - job tags scrapped from web
    :param type: string
    :param name: company - name of company
    :param type: string
    :param name: location - location scrapped from web
    :param type: string 
    :param name: salary - salary scrapped from web
    :param type: string
    :param name: link - link to apply for job
    :param type: string
    :param name: experience - experience if any scrapped from web
    :param type: string
    :param name: content - content in the job card scrapped from web
    :param type: string
    :param name: date - date on which we added the job to the database
    :param type: object of date
    """
    job_title=models.CharField(max_length=30)
    tag=models.CharField(max_length=50)
    company=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    salary_range=models.CharField(max_length=50)
    link=models.CharField(max_length=200)
    experience=models.CharField(max_length=30)
    content=models.CharField(max_length=200)
    date=models.DateField(blank=True,default=date.today)
