from requests.sessions import session
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import nltk
from LinkedInLogin import LinkedInLogin
import re
from datetime import date


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

email = "zxwind66@gmail.com"
password = "Testtest123"

#run login and return driver
wd=LinkedInLogin().run(email,password)


url_LA='https://www.linkedin.com/jobs/search/?f_JT=F&f_T=9%2C25201%2C3172&f_TPR=r86400&geoId=90000049&keywords=software%20engineer&location=Los%20Angeles%20Metropolitan%20Area&sortBy=R'
url_remote='https://www.linkedin.com/jobs/search/?f_JT=F&f_T=9%2C25201%2C25194%2C3172&f_TPR=r86400&f_WRA=true&geoId=103644278&keywords=software%20engineer&location=United%20States&sortBy=R'

wd.get(url_remote)
try:
    WebDriverWait(wd,5).until(EC.presence_of_element_located((By.CLASS_NAME, 'occludable-update')))
except TimeoutException:
    wd.quit()
    pass 

#number of jobs in LA 
no_of_jobs_LA = wd.find_element_by_tag_name('small').get_attribute('innerText')
no_of_jobs_LA=int(no_of_jobs_LA.split(' ')[0])


#Load job details into Dataframe
job_title = []
job_company = []
job_location = []
job_details = []
job_link=[]
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

#Browse all the jobs
i = 1
while i <= int(no_of_jobs_LA/25)+1: 
    #find jobs on each page
    jobs = wd.find_elements_by_class_name("occludable-update")

    #store title,company,location,link and job description information
    for job in jobs:
        wd.execute_script("arguments[0].scrollIntoView();", job)
        job.click()
        time.sleep(5)
        try:
            WebDriverWait(wd,5).until(EC.presence_of_element_located((By.ID, 'job-details')))
        except TimeoutException:
            wd.quit()
            pass 
        details=wd.find_element_by_id("job-details").text
        
        p=nltk.word_tokenize(details)
        try:
            index=p.index('years')
            if p[index-2]=='+':
                yearsofexperience=p[index-3]
            else:
                yearsofexperience=p[index-2]
            if int(yearsofexperience)>2:
                continue
        except ValueError:
            pass
        print(job.text)
        [title,company,location]=re.split('\n|-', job.text)[:3]
        link=job.find_element_by_class_name('job-card-container__link').get_attribute('href')
        job_link.append(link)
        job_title.append(title)
        job_company.append(company)
        job_location.append(location)
        job_details.append(details)
    try:
        wd.find_element_by_xpath(f"//button[@aria-label='Page {i}']").click()
        time.sleep(3)
    except:
        pass
        time.sleep(3)
    i = i + 1


#load data into a DataFrame
job_data = pd.DataFrame({
    'Company': job_company,
    'Title': job_title,
    'Location': job_location,
    'Description': job_details,
    'Link':job_link
})

# cleaning description column
job_data['Description'] = job_data['Description'].str.replace('\n',' ')
today=date.today()
job_data.to_excel('LinkedIn Job Data_Remote_'+str(today)+'.xlsx', index = False)