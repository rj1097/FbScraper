import mysql.connector
from mysql.connector import Error
import pandas as pd
from config import host, user, passwd, database


class db:

    def __init__(self):
        # config.__init__(self)
        self.dbConnect()

    def dbConnect(self):
        # Database Configuration Settings
        #check = [self.host,self.user,self.passwd,self.database]
        # print(check)
        # dbconfig = config()

        self.dbConnector = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )

        # Returns the connection object.
        # This object is required whenever you want to perform a select operation
        # or make any inserts/updates/deletes to the database
        # return mydb

    def select_all(self, table, where="", attempt=0):
        #print("SELECT * FROM " + table + " " + where)
        try:
            cursor = self.dbConnector.cursor()
            print("SELECT * FROM " + table + " " + where)
            cursor.execute("SELECT * FROM " + table + " " + where)

            row = cursor.fetchall()

            total = cursor.rowcount

            return [row, total]

        except Error as e:
            print("Task incomplete retrying !!!")
            print("Error in dbConnect")
            print(e)
            # print(type(attempt))
            if attempt < 5:
                self.dbConnect()
                print("DbConnectObject:", self.dbConnector)
                return self.select_all(table, where, attempt+1)
            else:
                print(
                    "--------------------------------------------------------------------")
                print("Unable to insert")
                print(
                    "--------------------------------------------------------------------")
                return [[], 0]

        else:
            cursor.close()

        # finally:
            # cursor.close()

    def select(self, table, col, where="", attempt=0):
        #print("SELECT * FROM " + table + " " + where)
        try:
            cursor = self.dbConnector.cursor()
            # print("SELECT `"+col+"` FROM `" + table + "` WHERE " + where)
            cursor.execute("SELECT `"+col+"` FROM `" +
                           table + "` WHERE" + where)

            row = cursor.fetchall()

            total = cursor.rowcount

            return [row, total]

        except Error as e:
            print("Task incomplete retrying !!!")
            print("Error in dbConnect")
            print(e)
            # print(type(attempt))
            if attempt < 5:
                self.dbConnect()
                print("DbConnectObject:", self.dbConnector)
                return self.select(table, col, where, attempt+1)
            else:
                print(
                    "--------------------------------------------------------------------")
                print("Unable to insert")
                print(
                    "--------------------------------------------------------------------")
                return [[], 0]

        else:
            cursor.close()

    def update(self, table, col, val, where="", attempt=0):
        #print("SELECT * FROM " + table + " " + where)
        try:
            cursor = self.dbConnector.cursor()
            print("UPDATE `"+table+"` SET `" + col +
                  "` = '" + val + "' WHERE " + where)

            cursor.execute("UPDATE `"+table+"` SET `" + col +
                           "` = '" + val + "' WHERE " + where)

            self.dbConnector.commit()

            return cursor.rowcount

        except Error as e:
            print("Task incomplete retrying !!!")
            print("Error in dbConnect")
            print(e)
            # print(type(attempt))
            if attempt < 5:
                self.dbConnect()
                print("DbConnectObject:", self.dbConnector)
                self.update(table, col, val, where, attempt+1)
                return 1
            else:
                print(
                    "--------------------------------------------------------------------")
                print("Unable to insert")
                print(
                    "--------------------------------------------------------------------")
                return 0

        else:
            cursor.close()
            return 1
    # def closeCursor(self):
    #     try:
    #         cursor = self.dbConnector.cursor()
    #         cursor.close()
    #     except Error as e:
    #         print(e)

    # UPDATE `linkedin_Scraper_Profiles` SET `Email` = 'brcgrrsn@protonmail.com' WHERE `linkedin_Scraper_Profiles`.`Email` = 'brcgrrsn@gmail.com';
    def delete(self, table, where=""):
        #print("SELECT * FROM " + table + " " + where)
        try:
            cursor = self.dbConnector.cursor()
            #print("SELECT `"+col+"` FROM `" + table + "` WHERE " + where)
            print("DELETE FROM `"+table+"` WHERE " + where)
            cursor.execute("DELETE FROM `"+table+"` WHERE " + where)

            self.dbConnector.commit()

            return cursor.rowcount

        except Error as e:
            print("Task Incomplete")
            print(e)

        else:
            cursor.close()

    def closeDb(self):
        cursor = self.dbConnector.cursor()
        cursor.close()

    # This function inserts all the rows to the specific table
    # Arguments Required -
    # 1. Connection Object
    # 2. Table Name
    # 3. Where Condition statment (Optional) - This is the where statement you can use to filter the results from the
    #    select query
    def insert(self, values, entity, attempt=0):
        try:
            cursor = self.dbConnector.cursor()
            #print("Using Dbconnector :",self.dbConnector)

            # add object to the tables

            add = {
                "fb_group_posts": ("INSERT INTO fb_group_posts "
                                   "(`Facebook Post ID`, `Facebook Post Content`, `Post DateTime`, `Posted By`, `Live Session Video`,`Group ID`) "
                                   "VALUES (%s, %s, %s, %s, %s,%s)"),

                "fb_group_post_comments": ("INSERT INTO fb_group_post_comments "
                                           "(`Comment ID`, `Comment Post ID`, `Comment Posted DateTime`, `Reply`, `Parent Comment ID`, `Posted By`, `Comment Content`) "
                                           "VALUES (%s, %s, %s, %s, %s, %s, %s)"),

                "fb_group_posts_reactions": ("INSERT INTO fb_group_posts_reactions "
                                             "(`Reaction ID`, `Facebook Post ID`, `Scraped DateTime`, `Posted By`) "
                                             "VALUES (%s, %s, %s, %s)"),

                "fb_group_posts_seen": ("INSERT INTO fb_group_posts_seen "
                                        "(`Seen ID`, `Facebook Post ID`, `Scraped DateTime`, `Posted By`, `Seen Status`) "
                                        "VALUES (%s, %s, %s, %s, %s)"),

                "fb_group_name": ("INSERT INTO fb_group_name "
                                  "(`User ID`, `Name`) "
                                  "VALUES (%s, %s)")
            }

            cursor.execute(add[entity], values)
            #print(add[entity], values)

            self.dbConnector.commit()
            return 1
        except Error as e:

            print("Task incomplete retrying !!!")
            print("Error in dbConnect")
            print(e)
            # print(type(attempt))
            if attempt < 5:
                self.dbConnect()
                print("DbConnectObject:", self.dbConnector)
                self.insert(values, entity, attempt+1)
                return 1
            else:
                print(
                    "--------------------------------------------------------------------")
                print("Unable to insert")
                print(
                    "--------------------------------------------------------------------")
                return 0

        else:
            #result = cursor.rowcount
            cursor.close()
            return 1


# def main():
#     dbobject = db()
#     print(dbobject.dbConnector)

# if __name__== "__main__":
#     main()
