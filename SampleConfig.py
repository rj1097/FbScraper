import os

# Add mysqldump to path
# Database creadentials
host = "***************"
user = "***************"
passwd = "***************"
database = "***************"

# Facebook Id and password
fbId = "***************"
fbPasswd = "***************"

# Chromedriver path
# Change it to wherever it is placed
driverPath = os.getcwd() + "\\chromedriver.exe"

# Group element Id
fbGroupId = "***************"

ProfilesPerId = 10
PostsPerId = 2

# Total posts to scrape at one go
totalPosts = 100
loginAttemptNo = 1
post_scrape_attempt_no = 3
