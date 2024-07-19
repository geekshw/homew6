# import sqlite3

# class Database:
#     def __init__(self, db_file):
#         self.conection = sqlite3.connect(db_file)
#         self.cursor = self.conection.cursor()
#     def create_table(self):
#         with self.conection:
#             self.cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS users(
#                     id INTEGER PRIMARY KEY AUTOINCREMENT ,
#                     user_id INTEGER NOT NULL ,
#                     username TEXT

#                 )
#             """)
#     def add_user(self, user_id , username):
#         with self.conection:
#             self.cursor.execute("INSERT INTO users (user_id,username) VALUES(?,?)",(user_id , username))

#     def get_user(self , user_id):
#         with self.conection:
#             return self.cursor.execute("SELECT * FROM users WHERE user_id = ?" , (user_id)).fetchone()
        