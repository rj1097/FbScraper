from config import driverPath, fbId, fbPasswd, fbGroupLink, totalPosts
# from dbConnect import
from scrapperFunctions import *
from time import sleep


class fb_login(scrapperFunctions):
    def __init__(self):
        self.loadFb()
        sleep(5)
        self.visitGroup()
        self.LoadGroup()

    def loadFb(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("-incognito")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            "E:\\FbScraper\\chromedriver.exe", options=chrome_options)
        self.login()

    def login(self):
        self.driver.get("https://facebook.com")
        self.find_elem_by_name("email").send_keys(fbId)
        self.find_elem_by_name("pass").send_keys(fbPasswd)
        self.find_elem_by_id("loginbutton").click()

    def visitGroup(self):
        # self.find_elem_by_link_text_with_wait(fbGroupName).click()
        self.driver.get(fbGroupLink)
        # self.find_elem_by_id_with_wait(fbGroupId).click()

    def LoadGroup(self, totalPosts=totalPosts):
        # self.visitGroup()
        self.postElements = self.find_elems_by_class_name_with_wait("_4mrt")
        count = 0
        oldPostsLoaded = 0
        while (count < 2) & (len(self.postElements) <= totalPosts):
            self.postElements = self.find_elems_by_class_name_with_wait(
                "_4mrt")
            ChangeInPostsNo = len(self.postElements) - oldPostsLoaded
            print("Change:", ChangeInPostsNo)
            if ChangeInPostsNo == 0:
                count += 1
                sleep(2)
                print("No new Post, Check:", count)
            else:
                count = 0
            oldPostsLoaded = len(self.postElements)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)

        print("Totalsposts:", len(self.postElements))
        print("All posts loaded")

    def logout(self):
        sleep(5)
        self.find_elem_by_id_with_wait("userNavigationLabel").click()
        self.find_elem_by_class_name_with_wait("_64kz").click()
