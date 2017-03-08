
"""
@author: dayle_fernandes
"""
#Currently only works with CS4296 Course on Canvas 

#Please ensure you have Selenium, BeautifulSoup installed on your PC before executing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys




#Canvas Login URL
URL = "https://canvas.cityu.edu.hk/login/ldap"

#URL for labs and Lecture Notes respectively. if your course has same layout on Canvas as CS4296, you can replace the following URLS
course_files= "https://canvas.cityu.edu.hk/courses/15992/files/folder/lectures"
course_labs = "https://canvas.cityu.edu.hk/courses/15992/files/folder/labs"

#ID fields of password and login fields on canvas
login_field = "pseudonym_session_unique_id"
pwd_field = "pseudonym_session_password"

#Enter your Canvas Credentials here
uname_credentials = "aname"
passw_credentials = "apass"

#Path to the downloaded chrome driver. PLease add the path to your chrome driver for script to work . Ensure 'r' is added before path for script to work 
chrome_path = r"path/to/chrome/webdriver"

#Changing Chrome Driver default directory 
chrome_option =webdriver.ChromeOptions()

#If you wish to change download directory, change the second parameter of following line. Ensure 'r' is added before path for script to work
prefs = prefs = {"download.default_directory" : r"path/to/desired/download/directory"}
chrome_option.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_option)
driver.get(URL)

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
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'ef-name-col__text')))
    r = driver.page_source
    return r

#Download module, searches for every relavent link and downloads the files
def download(source):
    soup = BeautifulSoup(source,"lxml")
    for link in soup.find_all('a',class_='ef-name-col__link'):
        driver.get(link.get('href'))

#Self Explanitory
def download_files(url):
    pg_src = navigate(url)
    download(pg_src)


#Calling necessary modules for script to run 
login(uname_credentials,passw_credentials,login_field, pwd_field)
download_files(course_files)
download_files(course_labs)

#debug
#for link in soup.find_all('a', class_='ef-name-col__link'):
#    print(link.get('href'))
