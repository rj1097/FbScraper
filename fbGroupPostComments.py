from fbLogin import *
from xpaths import *
from dbConnect import db
from scrapperFunctions import *
from datetime import datetime, date, timedelta
import numpy as np
from tqdm import tqdm
import time
# import random


class fb_group_post_comments(scrapperFunctions):
    def __init__(self, fbObject):
        self.driver = fbObject.driver

    def comment_by(self, commentElement):
        commentByIdElement = self.find_elem_by_xpath_with_wait("." + commentByIdElementXpath, commentElement)
        # if commentByNameElement == None:
        #     commentByNameElement = self.find_elem_by_xpath_with_wait(commentByNameElementXpath2, commentElement)

        # commentByLink = self.find_elem_by_xpath_with_wait("_5pb8",commentByNameElement).get_property("href")
        try:
            href = commentByIdElement.get_attribute("href")
            href = href.strip("https://www.facebook.com/")
            commentById = ""
            if "?id=" in href:
                commentById = href.split("?id=")[1].split("&")[0]
            else:
                commentById = href.split("?")[0]
            # commentBy = commentByNameElement.get_attribute("data-hovercard").split("=")[1].split("&")[0]
            return commentById
        except:
            return ""

    def comment_by_name(self, commentElement):
        commentByNameElement = self.find_elem_by_xpath_with_wait("." + commentByNameElementXpath, commentElement)
        # if commentByNameElement == None:
        #     commentByNameElement = self.find_elem_by_xpath_with_wait(commentByNameElementXpath2, commentElement)

        # commentByLink = self.find_elem_by_xpath_with_wait("_5pb8",commentByNameElement).get_property("href")
        commentByName = commentByNameElement.text
        return commentByName

    def comment_timestamp(self, commentElement, yr):
        self.scroll_to_element(commentElement)
        count = 0
        commentTime = ""
        while(count < 5):
            try:
                self.scroll_to_element(commentElement)
                timestampElement = self.find_elem_by_xpath_with_wait("." + commentTimestampXpath, commentElement)
                self.move_to_element(timestampElement)
                try:
                    commentTimeElement = self.find_elem_by_xpath_with_wait("." + toolTipXpath)
                except: 
                    commentTimeElement = self.find_elem_by_xpath_with_wait(toolTipXpath)
                # print(commentTimeElement.text)
                commentTime = commentTimeElement.text
                dateTime = parse(commentTime)
                dateTime.replace(year=int(yr))
                dateTime = dateTime.timestamp()
                break
            except:
                time.sleep(1 * count)
                count += 1
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            #     # print("Retry #",count)
        if(count >= 5):
            raise
        # dateTime = int(convert_to_timestamp(commentTime, year))
        return dateTime

    # def comment_timestamp(self, postElement, commentIdx):
    #     commentElements = self.find_elem_by_xpath_with_wait(postElement, "." + commentElementXpath)
        

    def comment_at(self, commentElement,year):
        try:
            timestamp = int(self.comment_timestamp(commentElement,year))
        except:
            timestamp = 0
        return datetime.fromtimestamp(timestamp).isoformat()

    def comment_content(self, commentElement):
        try:
            return self.find_elem_by_xpath_with_wait("." + commentContentXpath, commentElement).text
        except:
            return "INVALID TEXT"

    def find_parent_comment_element(self, comment_elements, cIdx):
        # print(child_comment.text)
        # cIdx = comment_elements.index(child_comment)
        try:
            for i in range(cIdx-1, -1, -1):
                label = comment_elements[i].get_attribute("aria-label").lower()
                if("reply" not in label):
                    return i

        except:
            return -1

    def total_comments_in_post(self, postElement):
        commentNoElement = self.find_elem_by_xpath_with_wait("." + commentNoElementXpath, postElement)
        # print("Total Comments:", commentNoElement.text)
        try:
            return int(commentNoElement.text.split(" comment")[0])
        except:
            return -1

    def select_most_recent_element(self, postElement):
        self.scroll_to_element(postElement)
        try:
            mostRelevantElement = self.find_elem_by_xpath_with_wait("."+mostRelevantElementXpath, postElement)
            # mostRelevantElement = postElement.find_element_by_xpath(mostRelevantElementXpath)
            # sleep_time = 2
            # while(mostRelevantElement.text != "Most recent"):
            # print(mostRelevantElement.text)
            # self.scroll_to_element(mostRelevantElement)
            mostRelevantElement.click()
            # sleep(sleep_time)
            # sleep_time *= 2

            newestElement = self.find_elems_by_xpath_with_wait(relevancyPopupXpath)[-1]
            # self.scroll_to_element(newestElement)
            newestElement.click()

            mostRelevantElement = self.find_elem_by_xpath_with_wait("."+mostRelevantElementXpath, postElement)
            mostRelevantElement = "Most Relevant"   

        except:
            print("No Relevancy Factor !!!")


    def load_all_comments(self, postElement):
        loadMoreElement = self.find_elems_by_xpath_with_wait("."+loadMoreElementXpath, postElement)
        seeMoreElement = self.find_elems_by_xpath_with_wait("."+seeMoreElementXpath, postElement)
        # loadMoreButtonElement = self.find_elem_by_xpath_with_wait("_4sxc",loadMoreElement[0])

        while(len(loadMoreElement) > 0 or len(seeMoreElement) > 0):

            # print(loadMoreElement)
            # loadMoreButtonElement = self.find_elem_by_xpath_with_wait("_4sxc",loadMoreElement[0])
            # if(loadMoreButtonElement == None):
            #     break
            try:
                loadType = loadMoreElement[-1].text.lower()
                if "hide" in loadType:
                    break
            except:
                # print("")
                temp = 1

            for load in loadMoreElement:    
                try:
                    self.scroll_to_element(load)
                    load.click()
                except:
                    continue

            for more in seeMoreElement:
                try:
                    self.scroll_to_element(more)
                    more.click()
                except:
                    continue
            
            loadMoreElement = self.find_elems_by_xpath_with_wait("."+loadMoreElementXpath, postElement)
            seeMoreElement = self.find_elems_by_xpath_with_wait("."+seeMoreElementXpath, postElement)

    def scrape_comments(self, postElement, postId, year = 2020):
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        mydb = db()
        self.scroll_to_element(postElement)
        total_comments_in_post = self.total_comments_in_post(postElement)
        if(total_comments_in_post != -1):
            self.select_most_recent_element(postElement)
            # postId = self.post_id(postElement)
            # total_comments_scraped = total_comments_scraped(postId)
            total_comments_scraped = 0
            print("Total Comments scraped :", total_comments_scraped)
            print("Total Comments :", total_comments_in_post)
            if(total_comments_in_post > total_comments_scraped):
                self.load_all_comments(postElement)
                commentElements = self.find_elems_by_xpath_with_wait("." + commentElementXpath, postElement)
                commentIds = []#scraped_comment_ids()
                memberIds = []#list(scraped_member_ids())
                print("Scraping comments")
                # for cIdx in tqdm(range(len(commentElements))):
                parentCommentDict = {}
                for cIdx in tqdm(range(len(commentElements))):
                    comment = commentElements[cIdx]
                    # print(comment.text)
                    commentBy = self.comment_by(comment)
                    commentTimestamp = self.comment_timestamp(comment, year)
                    commentContent = self.comment_content(comment)
                    commentId = generate_id(commentTimestamp, commentBy, commentContent)

                    # print("CommentId :",commentId)
                    if commentId not in commentIds:
                        commentLabel = comment.get_attribute("aria-label").lower()
                        if("reply" not in commentLabel):
                            isReply = "No"
                            parentCommentId = "None"
                            LastParentComment = comment
                        else:
                            isReply = "Yes"

                            # try:
                            #     parentCommentId = self.comment_by(LastParentComment)
                            # except:
                            pCIdx = self.find_parent_comment_element(commentElements, cIdx)
                            if pCIdx not in parentCommentDict:
                                try:
                                    parentCommentBy = self.comment_by(commentElements[pCIdx])
                                    parentCommentTimestamp = str(self.comment_timestamp(commentElements[pCIdx],year))
                                    parentCommentContent = self.comment_content(commentElements[pCIdx])
                                    parentCommentId = generate_id(parentCommentTimestamp, parentCommentBy, parentCommentContent)
                                    
                                except:
                                    parentCommentId = "NotFound"+"#"+postId
                                parentCommentDict[pCIdx] = parentCommentId
                            else:
                                parentCommentId = parentCommentDict[pCIdx]
                            
                        commentDateTime = self.comment_at(comment,year)
                        # commentBy = self.comment_by(comment)
                        if(commentBy not in memberIds):
                            memberIds.append(commentBy)
                            name = self.comment_by_name(comment)
                            mem_data = [str(commentBy), str(name)]
                            # mydb.insert(mem_data, "fb_group_name")
                            # print("New member")
                            # print(mem_data)
                        # commentContent = self.comment_content(comment)

                        commentParam = [commentId, postId, commentDateTime,
                                        isReply, parentCommentId, commentBy, commentContent]
                        # print(commentParam)
                        # mydb.insert(commentParam, "fb_group_post_comments")
                # mydb.closeCursor()
                    # print("####################################################################")
            else:
                print("No new comments !!")
        else:
            print("No comments present !!!")
        



# if __name__ == "__main__":
#     fb = fb_login()
#     fbComments = fb_group_post_comments(fb)
#     for postElem in fb.postElements:
#         scrape_comments(postElem)
