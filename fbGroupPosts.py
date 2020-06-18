from fbLogin import *
from config import fbGroupId
from dbConnect import db
from scrapperFunctions import *
from datetime import datetime
import numpy as np


class fb_group_posts(scrapperFunctions):
    def __init__(self, fbObject):
        self.driver = fbObject.driver

    def PostId(self, postElement):
        return postElement.get_attribute('id')
    def PostedBy(self, postElement):
        postedByNameElement = self.find_elem_by_class_name(
            "_5eit", postElement)
        postedByLink = self.find_elem_by_class_name(
            "_5pb8", postedByNameElement).get_attribute("data-hovercard")
        postedBy = postedByLink.split("=")[1].split("&")[0]
        return postedBy

    def PostedByName(self, postElement):
        return self.find_elem_by_class_name("_5pb8", postElement).get_attribute("title")

    def PostTimestamp(self, postElement):
        try:
            timestamp = int(self.find_elem_by_class_name(
                "_5ptz", postElement).get_attribute("data-utime"))
        except:
            timestamp = 0
        return datetime.fromtimestamp(timestamp).isoformat()

    def PostContent(self, postElement):
        postContent = []
        postDetails = self.find_elems_by_class_name_with_wait(
            "_5pbx", postElement)
        if len(postDetails) != 0:
            # self.CheckSeeMore(postElement)
            postContent.append(postDetails[0].text)
        else:
            postContent.append("No Content")
        # print(views)
        # print(i, ":", postContent[i])
        return postContent[0]

    def CheckSeeMore(self, postElement):
        # postElements = self.find_elems_by_class_name_with_wait("_4mrt")
        postDetails = self.find_elems_by_class_name_with_wait(
            "_5pbx", postElement)
        seeMoreLink = self.find_elems_by_class_name_with_wait(
            "text_exposed_hide", postDetails[0])
        if len(seeMoreLink) > 0:
            try:
                self.MoveToElement(seeMoreLink[-1])
                seeMoreLink[-1].click()
            except:
                # time.sleep(1)
                print("Some text hidden")
            # seeMoreLink[-1].click()
            # print(postDetails[0].text)

    def PostType(self, postElement):
        Posttype = []
        query = ["live", "QnA", "link", "unit",
                 "event", "Pre Recorded Video", "Query"]
        # PostsNo = len(postElements)
        # for i in range(PostsNo):
        PostTypeElement = self.find_elem_by_class_name_with_wait(
            "_5vra", postElement)
        # if len(PostTypeElements) > 0:
        if PostTypeElement != None:
            if query[0] in PostTypeElement.text:
                Posttype.append("Live Session")

            elif query[1] in PostTypeElement.text:
                Posttype.append("QnA Session")

            elif query[2] in PostTypeElement.text:
                Posttype.append("Link Shared")

            elif query[3] in PostTypeElement.text:
                Posttype.append("Unit Created")

            elif query[4] in PostTypeElement.text:
                Posttype.append("Event Created")

            elif query[5] in PostTypeElement.text:
                Posttype.append("Pre Recorded Video Posted")

            elif query[6] in PostTypeElement.text:
                Posttype.append("Query Made")

            else:
                Posttype.append("Regular Posts")
        else:
            Posttype.append("Not a Post")
        return Posttype[0]

    def load_posts(self, postElement):
        self.MoveToElement(postElement)
        postIds = scrapedPostsId()
        Id = self.PostId(postElement)
        if(Id not in postIds):
            seeMore = self.find_elems_by_class_name(
                "see_more_link", postElement)
            count = 0
            idx = 0
            while(len(seeMore) != 0):
                try:
                    self.MoveToElement(seeMore[idx])
                    seeMore[idx].click()
                except:
                    break
                currSeeMore = seeMore[0]
                seeMore = self.find_elems_by_class_name(
                    "see_more_link", postElement)
                if(currSeeMore == seeMore[0]):
                    print("Loading")
                    count += 1
                    sleep(2)
                else:
                    count = 0

                if count > 2:
                    print("Skipping load")
                    idx += 1
                else:
                    idx = 0

            # print("Inside the class")

            memberIds = scrapedMembersId()
            mydb = db()
            toInsertMemIds = []

            by = self.PostedBy(postElement)

            if(by not in memberIds):
                memberIds.append(by)
                name = self.PostedByName(postElement)
                mem_data = [by, name]
                mydb.insert(mem_data, "fb_group_name")
            time = self.PostTimestamp(postElement)
            content = self.PostContent(postElement)
            typePost = self.PostType(postElement)
            group_id = fbGroupId
            post_param = [Id, content, time, by, typePost, group_id]
            mydb.insert(post_param, "fb_group_posts")
            print(post_param)
        else:
            print("Post already scraped")
        # print("Post Data Loaded")
        # for post_data in post_params:

        # for mem_data in toInsertMemIds:

        # print("Post Data inserted in Database")


def scrapedPostsId():
    try:
        mydb = db()
        whereCondn = "1"
        postIds, size = mydb.select(
            "fb_group_posts", "Facebook Post ID", whereCondn)
        return np.array(postIds)[:, 0]
    except:
        return []


def scrapedMembersId():
    try:
        mydb = db()
        whereCondn = "1"
        postIds, size = mydb.select("fb_group_name", "User ID", whereCondn)
        return list(np.array(postIds)[:, 0])
    except:
        return []


if __name__ == "__main__":
    fb = fb_login()
    fbGrps = fb_group_posts(fb)
    # fbGrps.LoadGroup(50)
    postIds = scrapedPostsId()
    mydb = db()
    idx = 0
    for postElem in fb.postElements:
        print(idx)
        idx += 1
        Id = fbGrps.PostId(postElem)
        if(Id not in postIds):
            by = fbGrps.PostedBy(postElem)
            time = fbGrps.PostTimestamp(postElem)
            content = fbGrps.PostContent(postElem)
            typePost = fbGrps.PostType(postElem)
            mydb.insert([Id, content, time, by, typePost], "fb_group_posts")
