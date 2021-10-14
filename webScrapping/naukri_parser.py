import time
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

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
     "day":[]
     }

# df = pd.DataFrame(columns=['Title','Tag','Company','Location','Salary','Link','Experience','Content'])
link_desc={"link":[]}

def get_url(position,location):
    """Generate URL for particular job location and preference"""
    template = "https://www.naukri.com/data-scientist-jobs-in-indi?k={}&l={}"
    url = template.format(position,location)
    return url

def get_links(url):
    for i in range(0,1): 
        driver.get(url)
        # time.sleep(3)
        lst=driver.find_elements_by_class_name("jobTuple")

    for job in lst:
            # driver.implicitly_wait(3)
            link=job.find_element_by_class_name("title").get_attribute('href')
            link_desc["link"].append(link)


def get_data(link_desc , database):

    for lnk in link_desc["link"]:
        driver.get(lnk)
        time.sleep(3)
        lst2=driver.find_element_by_class_name("job-desc").text
        # date=""
        date = ""
        try:
            dateitwasposted = driver.find_element_by_class_name("stat").text
            for ele in dateitwasposted:
                if(ele.isdigit()):
                    date+=ele
            if(not date or int(date) >= 7):
                continue
            print(date) 
        except:
            date = "Not disclosed "
        print(date+"days ago")
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
            
            database["Title"].append(role)
            database["Tag"].append("hr")
            database["Company"].append(company)
            database["Salary"].append(salary)
            database["Link"].append(link_tojob)
            database["Experience"].append(experience)
            database["Content"].append(lst2)

            # database["day"].append()

            # print(len(database["Title"]))

    
        
url = get_url('senior accountant' , 'India')
get_links(url)
# print(link_desc)
get_data(link_desc , database)
for data in database["Title"]:
        print(data)
print(len(database["Title"]))


# print(database.to_string())
driver.quit()