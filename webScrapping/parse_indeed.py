import time
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import re

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install())


database ={"Title":[],
    "Tag":[],
     "Company":[],
     "Location":[],
     "Salary":[],
     "Link":[],
     "Experience":[],
     "Content":[],
     }

# df = pd.DataFrame(columns=['Title','Tag','Company','Location','Salary','Link','Experience','Content'])
link_desc={"link":[]}

def get_url(position,location):
    """Generate URL for particular job location and preference"""
    template = "https://in.indeed.com/jobs?q={}&l={}&start={}"
    start = 0
    url=[]
    for i in range(0,10):
       url.append(template.format(position,location , start))
       start += 10
    # print(url)
    return url

def get_links(url):
    for i in url: 
        # print(i)
        driver.get(i)
        # time.sleep(3)
        lst=driver.find_element_by_class_name("mosaic-provider-jobcards")
        links = lst.find_elements_by_class_name("tapItem")
        # print(links)
        for job in links:
            link_desc["link"].append(job.get_attribute('href'))
    
         
    print(len(link_desc["link"]))


def get_data(link_desc , database):
        for lnk in link_desc["link"]:
                driver.get(lnk)
                time.sleep(3)
                date_on_which_jobposted = driver.find_element_by_class_name("jobsearch-JobMetadataFooter").text
                date=""
                for ele in date_on_which_jobposted:
                    if(ele.isdigit()):
                        date+=ele
                if(not date or int(date) >= 7):
                    continue
                print(date)        
                # print(date_on_which_jobposted)
                role = driver.find_element_by_class_name("icl-u-xs-mb--xs").text
                # print(role , end= " ")
                company = driver.find_element_by_class_name("icl-u-lg-mr--sm").text
                # print(company ,end = " ")
                location = driver.find_elements_by_class_name("icl-u-xs-mt--xs")
                # print(location[0].text.split("\n")[1] ,end= "   "   )
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
                    # print(lowercase_str)
                    list = [m.start() for m in re.finditer('year', lowercase_str)]
                    if(list):
                        start = list[0]
                        for i in reversed(list):
                            # print(i)
                            if(lowercase_str[i-2].isdigit()):
                                exp = lowercase_str[start - 2:i+4]
                                break

                # print(exp)        

url = get_url('senior accountant' , 'India')
get_links(url)
get_data(link_desc,database)


# print(database.to_string())
driver.quit()