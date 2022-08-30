from time import sleep
import pandas as pd
import warnings
from retrying import retry
import math


warnings.filterwarnings('ignore')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# creating the instance of the browser
class jira_worklog:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self, username, password):
        self.open('https://id.atlassian.com/login')
        self.type('''//*[@id="username"]''', username)
        self.type('''//*[@id="username"]''', Keys.ENTER)
        self.type('''//*[@id="password"]''', password)
        self.click('''//*[@id="login-submit"]''')

    def log_time(self, ticket_link, date, time, description):
        #process
        self.open(ticket_link)
        #switch iframe
        sleep(2)
        self.change_iframe('''iframe[id*='clockwork-free-cloud__issue-worklog-content']''')
        #click + or add worklog button
        self.click('''//*[@id="content"]/div[1]/div[1]/div[2]/div/button/span/div/span''')
        #switch iframe to popup
        self.change_iframe('''iframe[id*='clockwork-free-cloud__log-work-dialog']''')
        #enter time spent
        self.type('''//*[@id="timeSpent-uid3"]''', time)
        #enter description
        self.type('''//*[@id="content"]/form/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[2]/p''', description)
        #date
        self.click('''//*[@id="content"]/form/div/div[4]/div[3]/div/div[1]/div[1]/div/div/div/div[1]''')    #click
        self.type('''//*[@id="react-select-started-uid7-input"]''', date)    #type
        self.type('''//*[@id="react-select-started-uid7-input"]''', Keys.ENTER)    #enter
        #click save
        self.click('''//*[@id="content"]/form/footer/div/div[1]/button/span''')

    @retry(wait_fixed=1000, stop_max_attempt_number=10)
    def open(self, link):
        self.driver.get(link)

    @retry(wait_fixed=1000, stop_max_attempt_number=100)
    def change_iframe(self, iframe_id):
        self.default_iframe()
        iframe = self.driver.find_element(By.CSS_SELECTOR,iframe_id)
        self.driver.switch_to.frame(iframe)

    @retry(wait_fixed=1000, stop_max_attempt_number=100)
    def click(self, element_id):
        self.driver.find_element(By.XPATH,element_id).click()

    @retry(wait_fixed=1000, stop_max_attempt_number=10)
    def type(self, element_id, value):
        self.driver.find_element(By.XPATH, element_id).send_keys(value)

    @retry(wait_fixed=1000, stop_max_attempt_number=10)
    def default_iframe(self):
        self.driver.switch_to.default_content()

    def close(self):
        self.driver.close()

    
