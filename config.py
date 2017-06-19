import MySQLdb


class Db:
    def __init__(self):
        self.host = 'localhost'
        self.name = 'atm_beras'
        self.username = 'root'
        self.password = 'bismillah'
        self.con = MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.name)

    def connect(self):
        return MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.name)