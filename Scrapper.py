from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time

class Scrapper:
    username_string = ""
    password_string = ""
    link_username = ""
    number_of_posts = 5
    SCROLL_PAUSE_TIME = 3
    userEmails = []
    newUsers = []
    previousUsers = []

    def __init__(self):
        self.credentials()
        self.init()
        self.login()


    def credentials(self):

        print("Shkruani username e Linkedin (email/username?):")
        self.username_string = str(input())
        print()
        print("Shkruani passwordin e Linkedin:")
        self.password_string = str(input())
        print()
        print("Shkruani usernamin tuaj:")
        self.link_username = str(input())
        print()
        # print("Shkruani numrin e posteve qe do te analizoni:")
        # self.number_of_posts = int(input())
    def init(self):
        ser = Service("./ChromeDriver.exe")
        op = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(service=ser, options=op)
    def login(self):

        self.browser.get('https://www.linkedin.com/login')
        elementID = self.browser.find_element_by_id('username')
        elementID.send_keys(self.username_string)
        elementID = self.browser.find_element_by_id('password')
        elementID.send_keys(self.password_string)
        elementID.submit()
        self.getData(self.link_username)

    def getData(self, username):

        recent_activity_link = "https://www.linkedin.com/in/"+username+"/"

        self.browser.get(recent_activity_link)

        # number_of_scrolls = -(-self.number_of_posts // 5)
        #
        # SCROLL_PAUSE_TIME = 5
        #
        # # Get scroll height
        # last_height = self.browser.execute_script("return document.body.scrollHeight")
        #
        # for scroll in range(number_of_scrolls):
        #     self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(SCROLL_PAUSE_TIME)
        #     new_height = self.browser.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break
        #     last_height = new_height

        src = self.browser.page_source

        soup = BeautifulSoup(src, 'html.parser')  # lxml

        people_you_may_know = soup.find_all('li', attrs={"class":"pv-browsemap-section__member-container"})

        for user in people_you_may_know:
            nextUser = "https://www.linkedin.com"+user.a['href']+"overlay/contact-info/"
            if ((user.a['href'][4:][:-1] not in (self.newUsers)) and (user.a['href'][4:][:-1] not in (self.previousUsers)) ):
                self.newUsers.append(user.a['href'][4:][:-1])
            else:
                continue
            self.browser.get(nextUser)

            src = self.browser.page_source
            userEmail = self.getUserEmail(src)
            if ((userEmail != None) and (userEmail not in self.userEmails) ):
                self.userEmails.append(userEmail)

            print (self.userEmails)
            print (self.newUsers)
        time.sleep(self.SCROLL_PAUSE_TIME)

        for newUser in self.newUsers:
            if (len(self.newUsers) > 0):
                self.previousUsers.append(self.newUsers[0])
                self.newUsers.pop(0)

            self.getData(newUser)

    def getUserEmail(self, src):

        soup = BeautifulSoup(src, 'html.parser')
        userEmail = soup.find_all("section", attrs={"class":'ci-email'})
        for user in userEmail:
            return user.a['href'][7:]

scrapper = Scrapper()