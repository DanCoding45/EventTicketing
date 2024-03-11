import sqlite3

class EventAccessServices:
    
    def get_events(self):
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        query = "SELECT * FROM events LIMIT 10"
        cursor.execute(query)
        
        events = cursor.fetchall()        
        conn.close()
        return events
        