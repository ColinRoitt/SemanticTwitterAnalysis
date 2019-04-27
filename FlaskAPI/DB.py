import mysql.connector as mariadb
import json
import pickle


class DB:
    def __init__(self):
        self.connDs = ['',
                       '', '']
        self.connection = None
        self.connect()

    def getProfile(self, PID):
        cursor = self.connection.cursor(prepared=True)
        sql_parameterized_query = """SELECT * FROM Profiles WHERE PID = %s"""
        cursor.execute(sql_parameterized_query, (PID,))
        result = cursor.fetchall()
        return result

    def getProfileTweets(self, PID):
        cursor = self.connection.cursor()
        sql_query = """SELECT * FROM Tweets WHERE PID = """ + PID
        cursor.execute(sql_query)
        results = cursor.fetchall()
        row_headers = [x[0] for x in cursor.description]
        # 6 columns
        data = []
        for row in results:
            data.append({row_headers[0]: row[0],
                         'key': 'P'+str(row[1]),
                         row_headers[2]: row[2],
                         row_headers[3]: str(row[3]),
                         row_headers[4]: str(row[4]),
                         row_headers[5]: str(row[5])})
        return json.dumps(data)

    def getProfiles(self):
        cursor = self.connection.cursor(prepared=True)
        sql_query = """SELECT * FROM Profiles"""
        cursor.execute(sql_query)
        results = cursor.fetchall()
        row_headers = [x[0] for x in cursor.description]
        # 6 columns
        data = []
        for row in results:
            data.append({'key': 'P'+str(row[0]),
                         row_headers[1]: row[1].decode(),
                         row_headers[2]: row[2].decode(),
                         row_headers[3]: row[3].decode(),
                         row_headers[4]: str(row[4]),
                         row_headers[5]: row[5]})
        return json.dumps(data)

    def updateProfile(self, PID, name, search, social, start, countPerDay):
        cursor = self.connection.cursor(prepared=True)
        sql_query = """UPDATE Profiles SET search=%s, social=%s, start=%s, countPerDay=%s WHERE PID=%s"""
        cursor.execute(sql_query,
                       (search, social, start, countPerDay, PID))
        print(cursor.rowcount, "record(s) affected")
        self.connection.commit()
        return 'added'

    # GET
    def getTasks(self, PID):
        cursor = self.connection.cursor(prepared=True)
        sql_parameterized_query = """SELECT * FROM Tasks WHERE PID = %s"""
        cursor.execute(sql_parameterized_query, (PID,))
        results = cursor.fetchall()
        row_headers = [x[0] for x in cursor.description]
        # 6 columns
        data = []
        for row in results:
            data.append({row_headers[0]: str(row[0]),
                         'key': 'P'+str(row[1]),
                         row_headers[2]: row[2].decode(),
                         row_headers[3]: row[3].decode(),
                         row_headers[4]: row[4].decode(),
                         row_headers[5]: str(row[5])})
        return json.dumps(data)

    def addProfile(self, name, search, social, start, countPerDay):
        # PID name search social start countPerDay
        cursor = self.connection.cursor(prepared=True)
        sql_parameterized_query = """
        INSERT INTO Profiles (name, search, social, start, countPerDay) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql_parameterized_query,
                       (name, search, social, start, countPerDay))
        self.connection.commit()
        return "Values added ID: " + str(cursor.lastrowid)

    def deleteProfile(self, PID):
        cursor = self.connection.cursor()
        sql_query = """DELETE FROM Tasks WHERE PID = """ + PID
        cursor.execute(sql_query)
        sql_query = """DELETE FROM Tweets WHERE PID = """ + PID
        cursor.execute(sql_query)
        sql_query = """DELETE FROM Profiles WHERE PID = """ + PID
        cursor.execute(sql_query)
        self.connection.commit()
        # print(cursor.rowcount, "record(s) affected")
        return PID + "deleted"

    def addTask(self, PID, name, classO, compariator, bound):
        # TaID	PID	name	class	compariator	bound
        cursor = self.connection.cursor(prepared=True)
        sql_parameterized_query = """
        INSERT INTO Tasks (PID, name, class, compariator, bound) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql_parameterized_query,
                       (PID, name, classO, compariator, bound))
        self.connection.commit()
        return "Values added ID: " + str(cursor.lastrowid)

    def deleteTask(self, PID, TID):
        cursor = self.connection.cursor(prepared=True)
        sql_query = """DELETE FROM Tasks WHERE PID = %s AND TaID = %s"""
        cursor.execute(sql_query, (PID, TID))
        self.connection.commit()
        print(cursor.rowcount, "record(s) affected")
        return PID + ' ' + TID + " deleted"

    def addTweet(self, TwID, PID, content, sentiment, certainty, dateGot):
        # TwID	PID	content	sentiment	certainty
        cursor = self.connection.cursor(prepared=True)
        sql_parameterized_query = """
        INSERT INTO Tweets (TwID, PID, content, sentiment, certainty, dateGot) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql_parameterized_query,
                       (str(TwID), str(PID), str(content), str(sentiment), str(certainty), str(dateGot)))
        self.connection.commit()
        # print(sql_parameterized_query)
        cursor.execute('SELECT content FROM Tweets WHERE TwID = '+TwID+' AND PID ='+PID)
        print()
        print('NEW')
        print(cursor.fetchall())
        return "Values added ID: " + str(cursor.lastrowid)

    def getSearch(self, PID):
        cursor = self.connection.cursor(prepared=True)
        sql_parameterized_query = """SELECT search FROM Profiles WHERE PID = %s"""
        cursor.execute(sql_parameterized_query, (PID,))
        result = cursor.fetchall()
        return result

    def getCountPerDay(self, PID):
        cursor = self.connection.cursor(prepared=True)
        sql_parameterized_query = """SELECT countPerDay FROM Profiles WHERE PID = %s"""
        cursor.execute(sql_parameterized_query, (PID,))
        result = cursor.fetchall()
        return result

    def tweetIsSaved(self, TwID):
        cursor = self.connection.cursor(prepared=True)
        sql_parameterized_query = """SELECT content FROM Tweets WHERE TwID = %s"""
        cursor.execute(sql_parameterized_query, (TwID,))
        result = cursor.fetchall()
        return len(result) > 0

    def getQuery(self, query, perams):
        cursor = self.connection.cursor(prepared=True)
        cursor.execute(query, perams)
        result = cursor.fetchall()
        return result

    # GET

    def connect(self):
        db = mariadb.connect(
            host='91.208.99.2', port='1211', db='colinroi_fyp', user='colinroi_fyp', passwd='35aeba8b9c')
        self.connection = db
        return 'Connected!'
