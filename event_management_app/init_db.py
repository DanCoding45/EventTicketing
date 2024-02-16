
import sqlite3

def init_db():
    
    connection = sqlite3.connect('database.db')
    print("DB connection established!")
    with open('schema.sql') as f:
        connection.executescript(f.read())        
    print("Users table set up!")
    
    connection.close()

