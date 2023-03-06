try:
    import sqlite3
except:
    import _sqlite3 as sqlite3

from random import randint as rn

# pK1zH2lI1vxM0x
me = 230915398


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("asu_bot.db")
        self.name = "users"
        self.day = 86400
        self.hour = 3600
        self.create_base()

    # id int group text p int
    # tg 130123 598 1 1
    # p 0 None
    # p 1 - bakalavr
    # p 2 - magistr
    # p 3 - asper
    # p 4 admin

    def create_base(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""CREATE TABLE users 
            (id int, gp text, level_e int, course int)""")
            self.add_student(230915398, str(598), 4, 3)

        except:
            return 0

    def add_student(self, id, username=None, group=-1, course=-1):

        cursor = self.conn.cursor()

        cursor.execute(f"INSERT INTO users VALUES ('{id}', '{username}', '{group}','{course}')")

        self.conn.commit()

    # get students_by_group
    def find_student_by_group(self, group):
        cursor = self.conn.cursor()

        sql = "SELECT id FROM users WHERE gp = {}".format(group)

        cursor.execute(sql)
        return cursor.fetchall()

    def find_student_by_level_eduaction(self, level):
        cursor = self.conn.cursor()

        sql = "SELECT id FROM users WHERE level_e ={}".format(level)

        cursor.execute(sql)
        return cursor.fetchall()

    def find_student_by_level_course(self, course):
        cursor = self.conn.cursor()

        sql = "SELECT id FROM users WHERE course ={}".format(course)

        cursor.execute(sql)
        return cursor.fetchall()

    def get_admins(self):
        cursor = self.conn.cursor()

        sql = "SELECT id FROM users WHERE level_e=4"

        cursor.execute(sql)

        b = cursor.fetchall()

        return b

    def get_all_student(self):
        cursor = self.conn.cursor()

        sql = "SELECT * FROM users"

        cursor.execute(sql)

        b = cursor.fetchall()

        return b


if __name__ == '__main__':
    pass
