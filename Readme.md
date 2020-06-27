# Facebook Group Scraper

This tool is made to micro-manage any facebook group. This tool uses selenium webdriver to scrape information from facebook group like post comments, post likes etc. This data is then stored in user's personal database for tracking interactions between group admin and members.

## How to use

1. Fork this repository and download the package.
2. Set up local environment for this package.
3. Install required python dependencies using `pip install -r requirements.txt` in the package's directory.
4. Create following tables in your database.
    
    - *fb_group_posts* using fb_group_posts.sql
    - *fb_group_post_comments* using fb_group_post_comments.sql
    - *fb_group_posts_reactions* using fb_group_posts_reactions.sql

5. Rename SampleConfig.py to config.py and make the following changes:

    - Add database related information.
    - Add facebook Id and password.
    - Add the exact facebook group link. 
    <!-- Incomplete -->
6. Install chrome (If not already installed) and note down the chrome version. Now download the appropriate chromedriver and put it inside the package folder.
7. Now you can run the python package.
    
    - Use the command `python -u "PATH_TO_FBSCRAPER"\main.py"`

