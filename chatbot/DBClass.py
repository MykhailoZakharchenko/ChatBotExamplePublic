import mysql.connector
from chatbot.credentials.credentials  import db_config

class DBrunner():
    'class initiate connect with MySQL db connection, select and insert data, also insert BLOB objects (images)'
    def __init__(self):
        self.conn = None
        self.cur = None

    def connectiondatabase(self):
        #print(db_config['host'],db_config['username'],db_config['password'],db_config['database'])
        try:
            self.mydb = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['username'],
            database=db_config['database'],
            password=db_config['password']
        )
        except:
            return False
        self.cur = self.mydb.cursor()
        return True

    def closedatabase(self):
        # Shut down the database
        if self.mydb and self.cur:
            self.cur.close()
            self.mydb.close()
        return True

    #Used to query table data
    def select(self, sql):
        self.connectiondatabase()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.closedatabase()
        return result

    def insert(self, sql):
        self.connectiondatabase()
        self.cur.execute(sql)
        result = self.cur.lastrowid
        self.closedatabase()
        return result

    def insertBlob(self, sql,values):
        self.connectiondatabase()
        self.cur.execute(sql,values)
        result = self.cur.lastrowid
        self.closedatabase()
        return result
