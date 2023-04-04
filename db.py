import sqlite3
from random import randint as rn

# Constants
DAY_IN_SECONDS = 86400
HOUR_IN_SECONDS = 3600

# pK1zH2lI1vxM0x
me = 230915398


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("asu_bot.db")
        self.create_base()

    def create_base(self):
        """
        Creates the `users` table if it does not exist, and adds a default student to the table.
        """

        try:
            with self.conn:
                self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS users (
                        id INTEGER, 
                        username TEXT, 
                        "group" TEXT, 
                        phone_number TEXT,
                        role TEXT
                    )""")
        except sqlite3.Error as e:
            print("An error occurred:", e)

        # self.add_student(230915398, "Vladimir", "598", "+79609566753", "admin")

    def add_student(self, chat_id, username, group, phone_number, role):
        """
        Adds a new student to the `users` table.
        """
        if not self.get_user(chat_id):
            try:
                with self.conn:
                    self.conn.execute(
                        "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                        (chat_id, username, group, phone_number, role)
                    )
            except sqlite3.Error as e:
                print("An error occurred:", e)
        else:
            print(f"User with chat_id {chat_id} already exists in the database.")

    def get_user(self, chat_id):
        """
        Retrieves a user from the `users` table by their chat ID.
        """
        try:
            with self.conn:
                cursor = self.conn.execute("SELECT * FROM users WHERE id=?", (chat_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return {"id": user_data[0],
                            "username": user_data[1],
                            "group": user_data[2],
                            "phone_number": user_data[3],
                            "role": user_data[4]
                            }
                else:
                    return None
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def find_students_by_field(self, field, value):
        """
        Finds students in the `users` table where the given `field` matches the given `value`.
        Returns a list of the matching students, where each student is in the format of `get_user`.
        """
        try:
            with self.conn:
                sql = f"SELECT * FROM users WHERE {field} = ?"
                cursor = self.conn.execute(sql, (value,))
                students = cursor.fetchall()
                return [{"id": s[0],
                         "username": s[1],
                         "group": s[2],
                         "phone_number": s[3],
                         "role": s[4]
                         } for s in students]
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def get_admins(self):
        """
        Finds all admin-level students in the `users` table.
        Returns a list of the matching students, where each student is in the format of `get_user`.
        """
        try:
            with self.conn:
                sql = "SELECT * FROM users WHERE group = ?"
                cursor = self.conn.execute(sql, ("admin",))
                admins = cursor.fetchall()
                return [{"id": a[0],
                         "username": a[1],
                         "group": a[2],
                         "phone_number": a[3],
                         "role": a[4]
                         } for a in admins]
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def get_all(self):
        """
        Retrieves all students from the base
        """
        try:
            with self.conn:
                sql = f"SELECT * FROM users"
                cursor = self.conn.execute(sql)
                users = cursor.fetchall()
                return [{"id": u[0],
                         "username": u[1],
                         "group": u[2],
                         "phone_number": u[3],
                         "role": u[4]
                         } for u in users]
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def update_user_group_by_id(self, chat_id, new_group):
        """
        Updates the group of a user in the `users` table by their chat ID.
        """
        try:
            with self.conn:
                self.conn.execute(
                    "UPDATE users SET 'group'=? WHERE id=?",
                    (new_group, chat_id)
                )
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def is_admin(self, chat_id):
        """
        Returns True if the user with the given chat_id has "admin" role, False otherwise.
        """
        user = self.get_user(chat_id)
        print(user["role"])
        if user and user["role"] == "admin":
            return True
        else:
            return False

    def update_user_role_by_id(self, chat_id):
        """
        Updates the role of a user in the `users` table by their chat ID to "admin".
        """
        try:
            with self.conn:
                self.conn.execute(
                    "UPDATE users SET role=? WHERE id=?",
                    ("admin", chat_id)
                )
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()


if __name__ == '__main__':
    d = DB()
    print(d.get_user(230915398))
    d.update_user_role_by_id(230915398)