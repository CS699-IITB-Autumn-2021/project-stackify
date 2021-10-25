"""
naukri_parser
---------------------------------------------------------
webscrapping code of naukri.com.The approach is ,for each job preference get all jobs links available on that page
and then for each job get the relevant feilds.
"""

import time
import datetime
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from jobHunt.models import Job


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install())


jobs_tags = [ "data-handling","senior-developer" , "senior-accountant" , "HR" ] 

def get_url(position , location , pagenumber):
    
    '''
    Make URL for  jobs present in particular job and location preferences on a given page number.
    :param name:position - string representation of job preferences
    :param type:string
    :param name:location - name of location where job requested
    :param type:string
    :param name:pagenumber - pagenumber from which data is collected
    :param type:int

    '''
    template = "https://www.naukri.com/{}-jobs-in-{}-{}"
    url = template.format(position,location,pagenumber)
    # print(url)
    get_links(url ,position)


def get_links(url , tag ):

    '''
    Get URLs of all jobs presented for particular job and tag preferences on a given page number.
    :param name:url - string representation of weblink
    :param type:string
    :param name:tag - name of job preference
    :param type:string representation of job preference
    '''
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
        
    get_data(link_desc , tag)           
  



def get_data(link_desc , tag):
    '''
    Extract data relevant data from jobs.
    :param name:link_desc - links of various jobs available
    :param type:list of links
    :param name:tag - name of job preference
    :param type:string representation of job preference
    '''
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

for ele in jobs_tags:
    print(ele)
    for i in range(0,2):
        get_url(ele , "India" , i+1)
driver.quit()

