from sqlite3 import *

connection = connect('DB/my-test.db')

# with connection:
#     connection.execute("""
#     CREATE TABLE Users(
#         user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#         user_email TEXT,
#         user_password TEXT
#     );
#     """)

# with connection:
#     connection.execute("""
#     CREATE TABLE Cars(
#         id_user INTEGER,
#         nosaukums TEXT,
#         nobraukums INTEGER,
#         datums TEXT,
#         CONSTRAINT user_fk FOREIGN KEY(id_user) REFERENCES Users(user_id)
#     );
#     """)

# with connection:
#     connection.execute("""
#     CREATE TABLE Connection(
#         connection_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#         id_user_connection INTEGER
#     );
#     """)
