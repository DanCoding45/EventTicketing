import sqlite3

class EventAccessServices:
        
    def get_events(self, category=None):
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        if category:
            print(category)
            query = "SELECT * FROM events WHERE category = ?"
            cursor.execute(query, (category, ))
        else:
            query = "SELECT * FROM events LIMIT 10"
            cursor.execute(query)
        
        events = cursor.fetchall()
        print(events)        
        conn.close()
        return events
        