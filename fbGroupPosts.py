from fbLogin import *
from config import *
from dbConnect import db
from scrapperFunctions import *
from datetime import datetime
import numpy as np


class fb_group_posts(scrapperFunctions):
    def __init__(self, fbObject):
        self.driver = fbObject.driver

    # def post_id(self, postElement):
    #     return postElement.get_attribute('id')

    def posted_by(self, postHeaderElement):
        postedById = postHeaderElement.find_element_by_xpath("." + postedByIdElementXpath)
        href = postedById.get_attribute("href")
        href = href.strip("https://www.facebook.com/")
        postedById = ""
        if "?id=" in href:
            postedById = href.split("?id=")[1].split("&")[0]
        else:
            postedById = href.split("?")[0]
        return postedById

    def posted_by_name(self, postHeaderElement):
        postedByNameElement = self.find_elem_by_xpath_with_wait("." + postedByNameElementXpath, postHeaderElement)
        postedByName = postedByNameElement.text
        return postedByName

    def post_timestamp(self, postHeaderElement):
        self.scroll_to_element(postHeaderElement)
        count = 0
        postTime = ""
        while(1):
            try:
                self.scroll_to_element(postHeaderElement)
                timestampElement = self.find_elem_by_xpath_with_wait("." + postTimestampXpath, postHeaderElement)
                self.move_to_element(timestampElement)
                try:
                    postTimeElement = self.find_elem_by_xpath_with_wait("." + toolTipXpath)
                except: 
                    postTimeElement = self.find_elem_by_xpath_with_wait(toolTipXpath)
                # print(postTimeElement.text)
                postTime = postTimeElement.text
                break
            except:
                # time.sleep(1)
                count += 1
                # print("Retry #",count)

        dateTime = int(convert_to_timestamp(postTime))
        return dateTime

    def posted_at(self, postHeaderElement):
        try:
            timestamp = int(self.post_timestamp(postHeaderElement))
        except:
            timestamp = 0
        return datetime.fromtimestamp(timestamp).isoformat()


    def post_content(self, postElement):
        postContent = ""
        postContentElement = self.find_elem_by_xpath_with_wait("." + postContentXpath, postElement)
        try:
            postContent += postContentElement.text
        except:
            print("No text Content")
        
        postContent += "----------IMAGE ALT------------"
        try:
            postImageElements = self.find_elems_by_xpath_with_wait("." + postContentImageXpath,postElement)
            for imageElement in postImageElements:
                postContent += imageElement.text
        except:
            print("No Image in post")
        
        postImageElements = self.find_elems_by_xpath_with_wait(".//img", postElement)
        for image in postImageElements:
            postContent += image.get_attribute("alt")

        return postContent

    def click_see_more(self, postElement):
        # postElements = self.find_elems_by_xpath_with_wait("."+"_4mrt")
        # postDetails = self.find_elems_by_xpath_with_wait("."+"_5pbx", postElement)
        seeMoreElement = self.find_elem_by_xpath_with_wait("."+seeMoreElementXpath, postElement)
        while seeMoreElement:
            try:
                self.move_to_element(seeMoreElement)
                seeMoreElement.click()
            except:
                # time.sleep(1)
                print("Some text hidden")
            seeMoreElement = self.find_elem_by_xpath_with_wait("."+seeMoreElementXpath, postElement)
            # seeMoreLink[-1].click()
            # print(postDetails[0].text)

    def post_type(self, postHeaderElement):
        Posttype = []
        query = ["live", "qna", "link", "unit",
                 "event", "pre recorded video", "query"]
        # PostsNo = len(postElements)
        # for i in range(PostsNo):
        # postHeaderElement = self.find_elem_by_xpath_with_wait("."+"_5vra", postElement)
        # if len(postHeaderElements) > 0:
        if postHeaderElement != None:
            if query[0] in postHeaderElement.text.lower():
                Posttype.append("Live Session")

            elif query[1] in postHeaderElement.text.lower():
                Posttype.append("QnA Session")

            elif query[2] in postHeaderElement.text.lower():
                Posttype.append("Link Shared")

            elif query[3] in postHeaderElement.text.lower():
                Posttype.append("Unit Created")

            elif query[4] in postHeaderElement.text.lower():
                Posttype.append("Event Created")

            elif query[5] in postHeaderElement.text.lower():
                Posttype.append("Pre Recorded Video Posted")

            elif query[6] in postHeaderElement.text.lower():
                Posttype.append("Query Made")

            else:
                Posttype.append("Regular Posts")
        else:
            Posttype.append("Not a Post")
        return Posttype[0]

    def scrape_posts(self, postElement):
        self.scroll_to_element(postElement)
        self.click_see_more(postElement)
        postIds = scraped_post_ids()
        postHeaderElement = self.find_elem_by_xpath_with_wait("." + postHeaderXpath, postElement)
        timestamp = self.post_timestamp(postHeaderElement)
        time = self.posted_at(postHeaderElement)
        by = self.posted_by(postHeaderElement)
        content = self.post_content(postElement)
        Id = generate_id(timestamp,by,content)

        self.postId = Id
        self.postYear = time.split("-")[0]
        
        if(Id not in postIds):
            memberIds = [] #scraped_member_ids()
            # mydb = db()
            # toInsertMemIds = []

            if(by not in memberIds):
                memberIds.append(by)
                name = self.posted_by_name(postHeaderElement)
                mem_data = [by, name]
                # mydb.insert(mem_data, "fb_group_name")
            typePost = self.post_type(postHeaderElement)
            group_id = (fbGroupLink.split("/groups/")[1]).strip('/')
            post_param = [Id, content, time, by, typePost, group_id]
            # mydb.insert(post_param, "fb_group_posts")
            print(post_param)
        else:
            print("Post already scraped")
        # print("Post Data Loaded")
        # for post_data in post_params:

        # for mem_data in toInsertMemIds:

        # print("Post Data inserted in Database")





# if __name__ == "__main__":
#     fb = fb_login()
#     fbGrps = fb_group_posts(fb)
#     # fbGrps.LoadGroup(50)
#     postIds = scraped_post_ids()
#     mydb = db()
#     idx = 0
#     for postElem in fb.postElements:
#         print(idx)
#         idx += 1
#         Id = fbGrps.post_id(postElem)
#         if(Id not in postIds):
#             by = fbGrps.posted_by(postElem)
#             time = fbGrps.post_timestamp(postElem)
#             content = fbGrps.post_content(postElem)
#             typePost = fbGrps.post_type(postElem)
#             mydb.insert([Id, content, time, by, typePost], "fb_group_posts")
