import sqlite3


def init_db():

    connection = sqlite3.connect("database.db")
    print("DB connection established!")
    with open("schema.sql") as file:
        connection.executescript(file.read())

    print("Users table set up!")
    print("event_hosts table set up!")
    print("messages table set up!")

    connection.close()
