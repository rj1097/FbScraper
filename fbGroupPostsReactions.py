from fbLogin import *
from config import *
from dbConnect import db
from scrapperFunctions import *
from datetime import datetime
import numpy as np
from pytz import timezone
from tqdm import tqdm


class fb_group_posts_reactions(scrapperFunctions):
    def __init__(self, fbObject):
        self.driver = fbObject.driver

    def post_id(self, postElement):
        return postElement.get_attribute('id')

    def timestamp(self):
        return int(datetime.timestamp(timezone("Asia/Kolkata").localize(datetime.now())))

    def curr_date_time(self):
        curr_timestamp = self.timestamp()
        return datetime.fromtimestamp(curr_timestamp).isoformat()

    def scrape_post_reactions(self, postElement):
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        reaction_element = self.find_elem_by_class_name_with_wait(
            "_3dlf", postElement)
        liked_by = []
        if reaction_element != None:
            self.scroll_to_element(reaction_element)
            reaction_element.click()

            liked_by_elements = self.find_elems_by_class_name_with_wait(
                "_5j0e")
            count = 0
            for element in liked_by_elements:
                # print(count)
                count += 1
                profile = element.find_element_by_css_selector("a")
                by = profile.get_attribute(
                    "data-hovercard").split("=")[1].split("&")[0]
                name = profile.get_attribute("title")
                liked_by.append([by, name])
                # liked_by.append("Invalid Id")
            webdriver.ActionChains(self.driver).send_keys(
                Keys.ESCAPE).perform()
        return liked_by

    def load_post_reactions(self, postElement):
        post_id = self.post_id(postElement)
        # try:
        mydb = db()
        self.move_to_element(postElement)

        scraped_date_time = self.curr_date_time()
        liked_by = self.scrape_post_reactions(postElement)
        scraped_id = scrapedReactionId()
        memberIds = scrapedMembersId()
        print("Scraping Reactions")
        for profile_idx in tqdm(range(len(liked_by))):
            profile = liked_by[profile_idx]
            reaction_id = profile[0]+"&"+post_id
            if(reaction_id not in scraped_id):
                if(profile[0] not in memberIds):
                    memberIds.append(profile[0])
                    mydb.insert(profile, "fb_group_name")
                reaction_param = [reaction_id, post_id,
                                  scraped_date_time, profile[0]]
                # print(reaction_param)
                mydb.insert(reaction_param, "fb_group_posts_reactions")
        mydb.closeCursor()
        # except:
        #     print("No reaction ",post_id)


def scrapedReactionId():
    try:
        mydb = db()
        whereCondn = "1"
        reaction_ids, size = mydb.select(
            "fb_group_posts_reactions", "Reaction ID", whereCondn)
        mydb.closeCursor()
        return np.array(reaction_ids)[:, 0]
    except:
        return []


def scrapedMembersId():
    try:
        mydb = db()
        whereCondn = "1"
        postIds, size = mydb.select("fb_group_name", "User ID", whereCondn)
        mydb.closeCursor()
        return list(np.array(postIds)[:, 0])
    except:
        return []


def totalReactionsScraped(postId):
    try:
        mydb = db()
        whereCondn = " `Facebook Post ID` = " + "'"+postId+"'"
        postIds, size = mydb.select(
            "fb_group_posts_reactions", "Reaction ID", whereCondn)
        mydb.closeCursor()
        return size
    except:
        return -1
