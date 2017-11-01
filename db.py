import MySQLdb

class Database:
    def __init__(self):
        self.host = config["db"]["host"]
        self.username = config["db"]["user"]
        self.password = config["db"]["pass"]
        self.name = config["db"]["name"]
        self.con = None
        self.cur = None

    def connect(self):
        if self.con == None:
            self.con = MySQLdb.connect(
                host=self.host,
                user=self.username,
                passwd=self.password,
                db=self.name
            )
        return self.con

    def query(self, query, param=None):
        self.con = self.connect()
        self.cur = self.con.cursor()
        self.cur.execute(query, param)
        return self.cur

    def fetchone():
        result = self.cur.fetchone()
        self.cur.close()
        self.con.close()
        return result

    def fetchall():
        result = self.cur.fetchall()
        self.cur.close()
        self.con.close()
        return result

    def save(self, query, param=None):
        self.con = self.connect()
        cur = self.con.cursor()
        cur.execute(query, param)
        cur.close()
        self.con.commit()
        self.con.close()
