"""
indeed parser
---------------------------------------------------------
webscrapping code of indeed.com.The approach is ,for each job preference get all jobs links available on that page
and then for each job get the relevant feilds.
"""
from logging import currentframe
import time
import datetime
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import re
from jobHunt.models import Job

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install())

link_desc={"link":[]}
jobs_tags = [ "data-handling","senior-developer" ] 


def get_url(position , location):
    '''
    Make URL for  jobs present in particular job and location preferences.
    :param name:position - string representation of job preferences
    :param type:string
    :param name:location - name of location where job requested
    :param type:string

    '''
    template = "https://in.indeed.com/jobs?q={}&l={}&start={}"
    start = 0
    url=[]
    for i in range(0,2):
       url.append(template.format(position,location , start))
       start += 10
    get_links(url , position)

def get_links(url , tag):
    '''
    Get URLs of all jobs presented for particular job and tag preferences on a given page number.
    :param name:url - string representation of weblink
    :param type:string
    :param name:tag - name of job preference
    :param type:string representation of job preference
    '''
    for i in url: 
        driver.get(i)
        lst=driver.find_element_by_class_name("mosaic-provider-jobcards")
        links = lst.find_elements_by_class_name("tapItem")
        for job in links:
            link_desc["link"].append(job.get_attribute('href'))
    get_data(link_desc ,tag)
    

def get_data(link_desc ,tag):
    '''
    Extract data relevant data from jobs.
    :param name:link_desc - links of various jobs available
    :param type:list of links
    :param name:tag - name of job preference
    :param type:string representation of job preference
    '''
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
    

for ele in jobs_tags:  
    # print(ele)
    url = get_url(ele , 'India')
driver.quit()