from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
# from datetime import datetime, date, timedelta
import hashlib
import time
from dbConnect import db
from dateparser import parse
from customlog import *

def scraped_comment_ids():
    try:
        mydb = db()
        whereCondn = "1"
        commentIds, size = mydb.select(
            "fb_group_post_comments", "Comment ID", whereCondn)
        return np.array(commentIds)[:, 0]
        mydb.closeCursor()
    except:
        return []


def total_comments_scraped(postId):
    try:
        mydb = db()
        whereCondn = "`Comment Post ID` = " + "'"+postId+"'"
        postIds, size = mydb.select(
            "fb_group_post_comments", "Comment ID", whereCondn)
        mydb.closeCursor()
        return size
    except:
        return -1
    
def scraped_reaction_id():
    try:
        mydb = db()
        whereCondn = "1"
        reactionIds, size = mydb.select(
            "fb_group_posts_reactions", "Reaction ID", whereCondn)
        mydb.closeCursor()
        return np.array(reactionIds)[:, 0]
    except:
        return []


def total_reactions_scraped(postId):
    try:
        mydb = db()
        whereCondn = " `Facebook Post ID` = " + "'"+postId+"'"
        postIds, size = mydb.select(
            "fb_group_posts_reactions", "Reaction ID", whereCondn)
        mydb.closeCursor()
        return size
    except:
        return -1


def scraped_member_ids():
    try:
        mydb = db()
        whereCondn = "1"
        postIds, size = mydb.select("fb_group_name", "User ID", whereCondn)
        return list(np.array(postIds)[:, 0])
        mydb.closeCursor()
    except:
        return []


def scraped_post_ids():
    try:
        mydb = db()
        whereCondn = "1"
        postIds, size = mydb.select(
            "fb_group_posts", "Facebook Post ID", whereCondn)
        return np.array(postIds)[:, 0]
    except:
        return []
        
def convert_to_timestamp(dateTimeString, year = ""):
    # if("today" in dateTimeString.lower() or "yesterday" in dateTimeString.lower()):
    #     if "yesterday" in dateTimeString.lower():
    #         dateTimeString = dateTimeString.lower().replace("yesterday",(date.today() - timedelta(1)).strftime('%A, %d %B %Y'))
    #     else:
    #         dateTimeString = dateTimeString.lower().replace("today",date.today().strftime('%A, %d %B %Y'))

    # try:
    #     dateTime = datetime.strptime(dateTimeString,'%A, %d %B %Y at %H:%M')
    # except:
    #     try:
    #         dateTime = datetime.strptime(dateTimeString,'%d %B %Y at %H:%M')
    #     except:
    #         dateTimeString = dateTimeString.replace("at", year + " at")
    #         try: 
    #             dateTime = datetime.strptime(dateTimeString,'%d %B %Y at %H:%M')
    #         except:
    #             dateTimeString += " " + year
    #             dateTime = datetime.strptime(dateTimeString,'%d %B %Y')
    dateTime = parse(dateTimeString)
    if(year != ""):
        yr = int(year)
        dateTime.replace(year=yr)
    dateTime = dateTime.timestamp()
    return dateTime

def generate_id(*argv):
    logging.info("Generating Id")
    strHash = ""
    for arg in argv:
        strHash += str(arg) + "&"
    hashId = hashlib.md5(strHash.encode()) 
    return hashId.hexdigest()

class scrapperFunctions:
    def move_to_element(self, elem,element = None):
        if(element == None):
            element = self.driver
        action = webdriver.common.action_chains.ActionChains(element)
        action.move_to_element(elem)
        # element.click()
        action.perform()

    def scroll_to_element(self, elem,element = None):
        if(element == None):
            element = self.driver
        x = elem.location['x']
        y = elem.location['y'] - 150

        element.execute_script("window.scrollTo("+str(x)+","+str(y)+");")

    def find_elem_by_id_with_wait(self, elem_id, element=None, timeout=1):
        if(element == None):
            element = self.driver
        try:
            elem = WebDriverWait(element, timeout).until(
                lambda x: x.find_element_by_id(elem_id))
            return elem
        except:
            return None

    def find_elem_by_link_text_with_wait(self, elem_id, element=None, timeout=1):
        if(element == None):
            element = self.driver
        try:
            elem = WebDriverWait(element, timeout).until(
                lambda x: x.find_element_by_link_text(elem_id))
            return elem
        except:
            return None

    def find_elem_by_id(self, elem_id, element=None):
        if(element == None):
            element = self.driver
        try:
            elem = element.find_element_by_id(elem_id)
            return elem
        except:
            return None

    def find_elem_by_name(self, elem_name, element=None):
        if(element == None):
            element = self.driver
        try:
            elem = element.find_element_by_name(elem_name)
            return elem
        except:
            return None

    def find_elem_by_class_name_with_wait(self, class_name, element=None, timeout=1):
        if(element == None):
            element = self.driver
        try:
            elem = WebDriverWait(element, timeout).until(
                lambda x: x.find_element_by_class_name(class_name))
            return elem
        except:
            return None

    def find_elems_by_class_name_with_wait(self, class_name, element=None, timeout=1):
        if(element == None):
            element = self.driver
        try:
            elems = WebDriverWait(element, timeout).until(
                lambda x: x.find_elements_by_class_name(class_name))
            return elems
        except:
            return []
    
    def find_elem_by_xpath_with_wait(self, xpath, element=None, timeout=1):
        if(element == None):
            element = self.driver
        try:
            elem = WebDriverWait(element, timeout).until(
                lambda x: x.find_element_by_xpath(xpath))
            return elem
        except:
            return None

    def find_elems_by_xpath_with_wait(self, x_path, element=None, timeout=1):
        if(element == None):
            element = self.driver
        try:
            elems = WebDriverWait(element, timeout).until(
                lambda x: x.find_elements_by_xpath(x_path))
            return elems
        except:
            return []

    def find_elem_by_class_name(self, class_name, element=None):
        if(element == None):
            element = self.driver
        try:
            elem = element.find_element_by_class_name(class_name)
            return elem
        except:
            return None
    
    def find_elems_by_class_name(self, class_name, element=None):
        if(element == None):
            element = self.driver
        try:
            elems = element.find_elements_by_class_name(class_name)
            return elems
        except:
            return []

    def find_elems_by_id(self, id, element=None):
        if(element == None):
            element = self.driver
        try:
            elems = element.find_elements_by_id(id)
            return elems
        except:
            return []

    def generate_user_id(self, N):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

    def infinite_scroll(self):
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script("return window.scrollY")

        y_idx = 100

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, "+str(y_idx)+");")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            y_idx = y_idx + 200

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return window.scrollY")
            if new_height == last_height:
                break
            last_height = new_height
