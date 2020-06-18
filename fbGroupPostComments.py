from fbLogin import *
from config import *
from dbConnect import db
from scrapperFunctions import *
from datetime import datetime
import numpy as np

class fb_group_post_comments(scrapperFunctions):
    def __init__(self, fbObject):
        self.driver = fbObject.driver

    def post_id(self,postElement):
        return postElement.get_attribute('id')

    def comment_by(self,commentElement):
        commentByNameElement = self.find_elem_by_class_name("_6w8_",commentElement)
        if commentByNameElement == None:
            commentByNameElement = self.find_elem_by_class_name("_6qw4",commentElement)
        
        # commentByLink = self.find_elem_by_class_name("_5pb8",commentByNameElement).get_property("href")
        commentBy = commentByNameElement.get_attribute("data-hovercard").split("=")[1].split("&")[0]
        return commentBy

    def comment_by_name(self,commentElement):
        commentByNameElement = self.find_elem_by_class_name("_6w8_",commentElement)
        if commentByNameElement == None:
            commentByNameElement = self.find_elem_by_class_name("_6qw4",commentElement)
        
        # commentByLink = self.find_elem_by_class_name("_5pb8",commentByNameElement).get_property("href")
        commentByName = commentByNameElement.text
        return commentByName

    def comment_timestamp(self,commentElement):
        return self.find_elem_by_class_name("livetimestamp",commentElement).get_attribute("data-utime")

    def comment_at(self,commentElement):
        try:
            timestamp = int(self.comment_timestamp(commentElement))
        except:
            timestamp = 0
        return datetime.fromtimestamp(timestamp).isoformat()

    def comment_content(self,commentElement):
        try:
            return self.find_elem_by_class_name_with_wait("_3l3x",commentElement).text
        except:
            return "INVALID TEXT"


    def find_parent_comment_element(self,comment_elements,child_comment):
        child_idx = comment_elements.index(child_comment)
        try:
            for i in range(child_idx-1,-1,-1):
                if(comment_elements[i].get_attribute("aria-label") == "Comment"):
                    return comment_elements[i]

        except:
            return None
                

    def totalCommentsInPost(self,postElement):
        commentNoElement = self.find_elem_by_class_name_with_wait("_1whp",postElement)
        try:
            return int(commentNoElement.text.split(" comment")[0])
        except:
            return -1
    def loadComments(self,postElement):
        mydb = db()
        self.ScrollToElement(postElement)
        
        total_comments_in_post = self.totalCommentsInPost(postElement)
        if(total_comments_in_post != -1):
            
            postId = self.post_id(postElement)
            total_comments_scraped = totalCommentsScraped(postId)
            print("Total Comments scraped :",total_comments_scraped)
            print("Total Comments :",total_comments_in_post)
            if(total_comments_in_post > total_comments_scraped):
                try:
                    mostRelevantElement = self.find_elem_by_class_name_with_wait("_6w1v",postElement)
                    sleep_time = 2
                    while(mostRelevantElement.text != "Newest"):
                        self.ScrollToElement(mostRelevantElement)
                        mostRelevantElement.click()
                        sleep(sleep_time)
                        sleep_time *= 2

                        NewestElement = self.find_elems_by_class_name_with_wait("_54ni")[-1]
                        self.ScrollToElement(NewestElement)
                        NewestElement.click()
                        mostRelevantElement = self.find_elem_by_class_name_with_wait("_6w1v",postElement)
                    mostRelevantElement = "Most Relevant"

                except:
                    print("No Relevancy Factor !!!")
                loadMoreElement = self.find_elems_by_class_name_with_wait("_4sxc",postElement)
                SeeMoreElement = self.find_elems_by_class_name("_5v47",postElement)
                # loadMoreButtonElement = self.find_elem_by_class_name("_4sxc",loadMoreElement[0])

                while(len(loadMoreElement) > 0):
                    
                        # print(loadMoreElement)
                        # loadMoreButtonElement = self.find_elem_by_class_name("_4sxc",loadMoreElement[0])
                        # if(loadMoreButtonElement == None):
                        #     break
                        for load in loadMoreElement:
                            try: 
                                self.ScrollToElement(load)
                                load.click()
                            except:
                                continue

                        for more in SeeMoreElement:
                            try: 
                                self.ScrollToElement(more)
                                more.click()
                            except:
                                continue

                        loadMoreElement = self.find_elems_by_class_name("_4sxc",postElement)
                        SeeMoreElement = self.find_elems_by_class_name("_5v47",postElement)
        
                commentElements = self.find_elems_by_class_name("_4eek",postElement)
                commentIds = scrapedCommentsId()
                memberIds = list(scrapedMembersId())
                for comment in commentElements:
                    #print(comment.text)
                    commentBy = self.comment_by(comment)
                    commentId = commentBy+"&"+self.comment_timestamp(comment)+"&"+postId
                    
                    #print("CommentId :",commentId)
                    if commentId not in commentIds:
                        commentLabel = comment.get_attribute("aria-label")
                        if(commentLabel == "Comment"):
                            isReply = "No"
                            ParentCommentId = "None"
                            LastParentComment = comment
                        else:
                            isReply = "Yes"
                            
                            # try:
                            #     ParentCommentId = self.comment_by(LastParentComment)
                            # except:
                            ParentCommentElement = self.find_parent_comment_element(commentElements,comment)
                            try:
                                ParentCommentId = self.comment_by(ParentCommentElement)
                                ParentCommentId +="&"+self.comment_timestamp(ParentCommentElement)+"&"+postId 
                            except:
                                ParentCommentId = "NotFound"+"#"+postId



                        
                        commentDateTime = self.comment_at(comment)
                        commentBy = self.comment_by(comment)
                        if(commentBy not in memberIds):
                            memberIds.append(commentBy)
                            name = self.comment_by_name(comment)
                            mem_data = [str(commentBy),str(name)]
                            mydb.insert(mem_data,"fb_group_name")
                        commentContent = self.comment_content(comment)

                        commentParam = [commentId,postId,commentDateTime,isReply,ParentCommentId,commentBy,commentContent]
                        print(commentParam)
                        mydb.insert(commentParam,"fb_group_post_comments")
            
            else:
                print("No new comments !!")
        else:
            print("No comments present !!!")
            
            


def scrapedCommentsId():
    try:
        mydb = db()
        whereCondn = "1"
        commentIds,size = mydb.select("fb_group_post_comments","Comment ID",whereCondn)
        return np.array(commentIds)[:,0]
    except:
        return []

def totalCommentsScraped(postId):
    try:
        mydb = db()
        whereCondn = " `Comment Post ID` = "+ "'"+postId+"'"
        postIds,size = mydb.select("fb_group_post_comments","Comment ID",whereCondn)
        return size
    except:
        return -1

def scrapedMembersId():
    try:
        mydb = db()
        whereCondn = "1"
        postIds,size = mydb.select("fb_group_name","User ID",whereCondn)
        return list(np.array(postIds)[:,0])
    except:
        return []

if __name__ == "__main__":
    fb = fb_login()
    fbComments = fb_group_post_comments(fb)
    for postElem in fb.postElements:
        loadComments(postElem)


