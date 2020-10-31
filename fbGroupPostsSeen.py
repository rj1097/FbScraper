from fbLogin import *
from config import *
from scrapperFunctions import *
from dbConnect import db
from datetime import datetime
import numpy as np
from pytz import timezone


class fb_group_posts_seen(scrapperFunctions):
    def __init__(self, fbObject):
        self.driver = fbObject.driver

    def post_id(self, postElement):
        return postElement.get_attribute('id')

    def timestamp(self):
        return int(datetime.timestamp(timezone("Asia/Kolkata").localize(datetime.now())))

    def curr_date_time(self):
        curr_timestamp = self.timestamp()
        return datetime.fromtimestamp(curr_timestamp).isoformat()

    def scrape_post_seen_data(self, postElement, counter=0):
        fbParticipantList = []
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        PostSeenElements = self.find_elems_by_class_name("_33zy", postElement)
        if(len(PostSeenElements) > 0):
            self.driver.execute_script(
                "window.scrollBy(document.body.scrollWidth,0);")
            self.move_to_element(PostSeenElements[0])
            PostSeenElements[0].click()
            sleep(1)
            SeenDialog = self.find_elems_by_class_name("_4-i2")
            self.driver.execute_script(
                "window.scrollBy(document.body.scrollWidth,0);")
            SeeMore = self.find_elems_by_id("group_seen_by_pager_seen")
            if len(SeeMore) > 0:
                # time.sleep(1)
                self.driver.execute_script(
                    "window.scrollBy(document.body.scrollWidth,0);")
                self.move_to_element(SeeMore[0])
                SeeMore[0].click()
            sleep(1)
            SeenNo = int((self.find_elems_by_class_name_with_wait(
                "_35zo")[0].text).split(" ")[-1])
            NotSeenNo = int((self.find_elems_by_class_name(
                "_35zo")[1].text).split(" ")[-1])
            # print(SeenNo,NotSeenNo)
            participantElements = self.find_elems_by_class_name_with_wait(
                "_4nel")
            for participant in participantElements:
                fbParticipantList.append(int(participant.get_attribute(
                    "data-hovercard").split("=")[1].split("&")[0]))

            webdriver.ActionChains(self.driver).send_keys(
                Keys.ESCAPE).perform()
        return fbParticipantList[:SeenNo], fbParticipantList[SeenNo:SeenNo+NotSeenNo]

    def load_posts_seen(self, postElement):
        # mydb = db()
        self.move_to_element(postElement)
        post_id = self.post_id(postElement)
        scraped_date_time = self.curr_date_time()
        seen_by, not_seen_by = self.scrape_post_seen_data(postElement)
        scraped_id = []  # scrapedSeenId()
        for profile in seen_by:
            seen_id = str(profile)+"&"+post_id
            if(seen_id not in scraped_id):
                seen_param = [seen_id, post_id,
                              scraped_date_time, profile, "SEEN"]
                print(seen_param)
                # mydb.insert(seen_param,"fb_group_posts_seen")
            # else:
                # updateRow(seen_id,"SEEN")

        for profile in not_seen_by:
            not_seen_id = profile+post_id
            if(not_seen_id not in scraped_id):
                not_seen_param = [not_seen_id, post_id,
                                  scraped_date_time, profile, "NOT SEEN"]
                print(not_seen_param)
                # mydb.insert(not_seen_param,"fb_group_posts_seen")


def scrapedSeenId():
    try:
        mydb = db()
        whereCondn = "1"
        commentIds, size = mydb.select(
            "fb_group_posts_seen", "Seen ID", whereCondn)
        return np.array(commentIds)[:, 0]
    except:
        return []


def updateRow(seen_id, Status="SEEN"):
    mydb = db()
    table = "fb_group_posts_seen"
    col = "Seen Status"
    val = Status
    condnVal = "'" + seen_id + "'"
    where = "`Seen ID` = "+condnVal
    mydb.update(table, col, val, where)
