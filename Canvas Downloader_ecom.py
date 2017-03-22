
"""
@author: dayle_fernandes
"""
#Currently only works with CS4286 Course on Canvas 

#Please ensure you have Selenium, BeautifulSoup installed on your PC before executing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import html
from lxml.etree import tostring
import pandas as pd



#Canvas Login URL
URL = "https://canvas.cityu.edu.hk/login/ldap"


course_files= "https://canvas.cityu.edu.hk/courses/15990/pages"


#ID fields of password and login fields on canvas
login_field = "pseudonym_session_unique_id"
pwd_field = "pseudonym_session_password"

#Enter your Canvas Credentials here
uname_credentials = "aname"
passw_credentials = "apassword"

#Path to the downloaded chrome driver 
chrome_path = r"path/to/chrome/driver"

#Changing Chrome Driver default directory 
chrome_option =webdriver.ChromeOptions()

#If you wish to change download directory, change the second parameter of following line. Ensure 'r' is added before path for script to work
prefs = prefs = {"download.default_directory" : r"path/to/download/directory"}
chrome_option.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_option)
driver.get(URL)

week_pages = []
#Login module, searches and adds necesary credentials 
def login(uname, pass_w, log_field, pass_field):
    username = driver.find_element_by_id(log_field)
    password = driver.find_element_by_id(pass_field)
    username.send_keys(uname)
    password.send_keys(pass_w)
    driver.find_element_by_class_name("Button--login").click()


#Navigate module, navigates to page where files are kept for download    
def navigate(url):
    driver.get(url)
    #Foloowing lines instruct Selenium to wait for the entire page to load. Without this correct source of page is not obtained
    wait = WebDriverWait(driver,10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'ic-Table--condensed')))
    r = driver.page_source
    return r

#Searches for relevant links of each week and adds to array 
def strip_page(url):
    src = navigate(url)
    soup = BeautifulSoup(src,"lxml")
    soup = BeautifulSoup(str(soup.find_all(class_="ic-Table--condensed")[0]),"lxml")
    table = html.fragment_fromstring(str(soup))
    
    for row in table.iterchildren():
        for cell in row.iterchildren():
            strn = tostring(cell[0])
            s = BeautifulSoup(strn,"lxml")
            for td in s.find_all("td"):
                week_link = td.a["href"]
                week_pages.append(week_link)    
    
    
#Iterate through all URLs for each week, get file URL and Download
def download():
    week_pages.remove(week_pages[0])
    for url in week_pages:
        driver.get(url)
        wait = WebDriverWait(driver,10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'show-content')))
        s = BeautifulSoup(driver.page_source,"lxml")
        data = s.find_all(class_="show-content")
        records = []
        for div in data:
            links = div.find_all('a')
            for a in links:
                records.append(a["href"])
            
        if(len(records)>0):
            df = pd.DataFrame(records)
            dwn_links = df[0].unique()
            for link in dwn_links:
                driver.get(link)

#Calling necessary modules for script to run 
login(uname_credentials,passw_credentials,login_field, pwd_field)
strip_page(course_files)
download()


