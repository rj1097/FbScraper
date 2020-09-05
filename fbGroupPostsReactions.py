from fbLogin import *
from xpaths import *
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

    def load_profiles(self,reactionFrameElement):
        profileElements = self.find_elems_by_xpath_with_wait("." + reactionFrameProfileXpath, reactionFrameElement)
        changeInPostNo = 1
        tries = 0
        while(changeInPostNo != 0 or tries < 3):
            totalProfiles = len(profileElements)
            if(totalProfiles == self.totalReactions):
                break
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", profileElements[-1])
            except:
                print("Stale Element Exception")
            profileElements = self.find_elems_by_xpath_with_wait("." + reactionFrameProfileXpath, reactionFrameElement)
            changeInPostNo = len(profileElements) - totalProfiles
            if(changeInPostNo == 0):
                tries += 1
                time.sleep(tries * 1)
                # print("Total Reactions :",len(profileElements))
            else:
                tries = 0
        return profileElements

    def load_post_reactions(self, reactionPane, tries = 0):
        try:
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            reaction_element = self.find_elem_by_xpath_with_wait("." + postReactionsElementXpath, reactionPane)
            likedBy = []
            if reaction_element != None:
                self.scroll_to_element(reaction_element)
                reaction_element.click()
                print(reaction_element.text)
                self.totalReactions = int(reaction_element.text)
                reactionFrameElement = self.find_elem_by_xpath_with_wait("." + reactionFrameXpath)
                profileElements = self.load_profiles(reactionFrameElement)
                count = 0
                for element in profileElements:
                    # print(count)
                    try:
                        count += 1
                        profile = self.find_elem_by_xpath_with_wait(".//a", element)
                        name = element.text
                        href = profile.get_attribute("href")
                        href = href.strip("https://www.facebook.com/")
                        By = ""
                        if "?id=" in href:
                            By = href.split("?id=")[1].split("&")[0]
                        else:
                            By = href.split("?")[0]
                        likedBy.append([By, name])
                    except:
                        # print("Invalid Profile")
                        temp = 1
                    # likedBy.append("Invalid Id")
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            return likedBy
        except:
            tries += 1
            if(tries > 3):
                return []
            else:
                self.load_post_reactions(reactionPane, tries)

    def scrape_post_reactions(self, postElement, postId):
        # try:
            # mydb = db()
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        self.scroll_to_element(postElement)

        scrapedDateTime = self.curr_date_time()
        reactionPaneElement = self.find_elem_by_xpath_with_wait("." + postReactionPaneXpath,postElement)
        likedBy = self.load_post_reactions(postElement)
        scrapedId = scraped_reaction_id()
        memberIds = [] #scraped_members_id()
        print("Scraping Reactions")
        # print(likedBy)
        for pIdx in tqdm(range(len(likedBy))):
            profile = likedBy[pIdx]
            reactionId = generate_id(profile[0],postId)
            if(reactionId not in scrapedId):
                if(profile[0] not in memberIds):
                    memberIds.append(profile[0])
                    # mydb.insert(profile, "fb_group_name")
                reactionParam = [reactionId, postId,scrapedDateTime, profile[0]]
                # print(reactionParam)
                # mydb.insert(reactionParam, "fb_group_posts_reactions")
        # mydb.closeCursor()
        # except:
        #     print("No reaction ",postId)

