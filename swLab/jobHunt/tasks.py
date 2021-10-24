from celery import shared_task
from jobHunt.models import Job
from django.core.mail import send_mail

from logging import currentframe
import time
import datetime
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from jobHunt.models import Job,Job_preference
import re

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install())

#naukri parser
def n_get_url(position , location , pagenumber):
    """Generate URL for particular job location and preference"""
    template = "https://www.naukri.com/{}-jobs-in-{}-{}"
    url = template.format(position,location,pagenumber)
    print(url)
    n_get_links(url ,position)


def n_get_links(url , tag ):
    for i in range(0,1): 
    
        driver.get(url)
        time.sleep(3)
        lst=driver.find_elements_by_class_name("jobTuple")
    link_desc={"link":[]}
  
    for job in lst:
            
            try:
                link=job.find_element_by_class_name("title").get_attribute('href')
                link_desc["link"].append(link)
            except :
                continue
        
    n_get_data(link_desc , tag)           
  



def n_get_data(link_desc , tag):

    for lnk in link_desc["link"]:
        # print(lnk)
        try:
            driver.get(lnk)
        except:
            continue
        time.sleep(3)
        lst2=driver.find_element_by_class_name("job-desc").text
        # date=""
        date = ""
        reqdate = datetime.datetime.now()
        try:
            dateitwasposted = driver.find_element_by_class_name("stat").text
            for ele in dateitwasposted:
                if(ele.isdigit()):
                    date+=ele
            if(not date or int(date) >= 7):
                continue
            # https://stackoverflow.com/questions/28268818/how-to-find-the-date-n-days-ago-in-python
            tod = datetime.datetime.now()
            d = datetime.timedelta(days = int(date))
            reqdate = tod - d
            
        except:
            date = "Not disclosed "
        # print(reqdate)
        # print(date+"days ago")
        index = 0
        lst1=driver.find_elements_by_class_name("top")
        for x in lst1:
            role=x.find_element_by_class_name("jd-header-title").text

            # print(role,end="  ")
            company=x.find_element_by_class_name("jd-header-comp-name").text
            # print(company,end=" ")
            location=x.find_element_by_class_name("location ").text
            # print(location , end=" ")
            experience=x.find_element_by_class_name("exp").text
            # print(experience, end=" ")
            salary=x.find_element_by_class_name("salary").text
            # print(salary, end=" ")
            link_tojob = lnk
            
            
        
            a = Job(job_title = role ,tag  = tag , company = company , location = location,salary_range = salary,link = link_tojob,
            experience = experience,content = lst2,date = reqdate )
            a.save()
            # database["day"].append()

            # print(len(database["Title"]))
    link_desc.clear()

#indeed parser
def i_get_url(position , location):
    """Generate URL for particular job location and preference"""
    template = "https://in.indeed.com/jobs?q={}&l={}&start={}"
    start = 0
    url=[]
    for i in range(0,2):
       url.append(template.format(position,location , start))
       start += 10
    i_get_links(url , position)

def i_get_links(url , tag):
    for i in url: 
        driver.get(i)
        lst=driver.find_element_by_class_name("mosaic-provider-jobcards")
        links = lst.find_elements_by_class_name("tapItem")
        for job in links:
            link_desc["link"].append(job.get_attribute('href'))
    i_get_data(link_desc ,tag)
    

def i_get_data(link_desc ,tag):
        for lnk in link_desc["link"]:
                driver.get(lnk)
                time.sleep(3)
                date_on_which_jobposted = driver.find_element_by_class_name("jobsearch-JobMetadataFooter").text
                date=""
                reqdate = datetime.datetime.now()
                for ele in date_on_which_jobposted:
                    if(ele.isdigit()):
                        date+=ele
                if(not date):
                    reqdate = datetime.datetime.now()
                elif(int(date) >= 7):
                    continue
                else:
                    tod = datetime.datetime.now()
                    d = datetime.timedelta(days = int(date))
                    reqdate = tod - d
                print(reqdate)        
                role = driver.find_element_by_class_name("icl-u-xs-mb--xs").text
                company = driver.find_element_by_class_name("icl-u-lg-mr--sm").text
                location = driver.find_elements_by_class_name("icl-u-xs-mt--xs")
                curent_location = location[0].text.split("\n")[1] 
                print(curent_location)
                try:
                    salary = driver.find_element_by_class_name("jobsearch-JobMetadataHeader-item").text
                except:
                    salary = "Not Disclosed"
                link_job = lnk
                jobDecsription = driver.find_element_by_class_name("jobsearch-jobDescriptionText").text
                index_for_exp_field = jobDecsription.find('Experience')
                exp = "Not mentioned"
                if(index_for_exp_field != -1):
                    lowercase_str = jobDecsription[index_for_exp_field + len('Experience') :len(jobDecsription)].lower()
                    list = [m.start() for m in re.finditer('year', lowercase_str)]
                    if(list):
                        start = list[0]
                        for i in reversed(list):
                            if(lowercase_str[i-2].isdigit()):
                                exp = lowercase_str[start - 2:i+4]
                                break
                
                a = Job(job_title = role ,tag  = tag , company = company , location = curent_location,salary_range = salary,link = lnk,
                experience = exp,content = jobDecsription,date = reqdate )
                a.save()

#notification
def notify():
    for user in Job_preference.objects.all():
        person=Seeker.objects.filter(email=user.email)
        person=person[0]
        mail_content="Hi aspirant!\n Here are some of the job notifications for you.\n"
        location=[]
        if(person.location1!='NA'):
            location.append(person.location1)
        if(person.location2!='NA'):
            location.append(person.location2)
        if(person.location2!='NA'):
            location.append(person.location2)
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        for job in Job.objects.filter(tag=user.job_title,date__range=(today_min, today_max)):
            for l in location:
                if(l in job.location):
                    mail_content+="location: "+job.location+"\ncompany name: "+job.company+"\nlink to apply: "+job.link+"\n\n"
        send_mail(
            'jobHunt Notification: '+user.job_title,
            mail_content,
            'aish8102000@gmail.com',
            [user.email],
            fail_silently=False,
        )

@shared_task
def periodic_update():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    jobs_tags = [ "data-handling","senior-developer" , "senior-accountant" , "HR" ] 
    
    for ele in jobs_tags:
        print(ele)
        for i in range(0,2):
            n_get_url(ele , "India" , i+1)
            
    link_desc={"link":[]}
    for ele in jobs_tags:  
        # print(ele)
        url = i_get_url(ele , 'India')
    driver.quit()
    
    notify()
