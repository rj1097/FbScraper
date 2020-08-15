from fbGroupPosts import fb_group_posts
from fbLogin import fb_login
from fbGroupPostComments import fb_group_post_comments
from fbGroupPostsReactions import fb_group_posts_reactions

if __name__ == "__main__":
    fb = fb_login()
    count = 1
    fbPosts = fb_group_posts(fb)
    fbReaction = fb_group_posts_reactions(fb)
    fbComments = fb_group_post_comments(fb)
    attempt = 0
    problematic_posts = []
    for post in fb.postElements[1:]:
        try:
            print("###############################################################")
            print("Post No. :", count)
            fbPosts.load_posts(post)
            fbComments.loadComments(post)
            fbReaction.load_post_reactions(post)
            count += 1
        except:
            problematic_posts.append(count-1)
    print(problematic_posts)
    fb.logout()
    fb.driver.close()
