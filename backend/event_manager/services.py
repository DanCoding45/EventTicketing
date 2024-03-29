
import sqlite3
from .models import EventGuest

class EventManagerServices:
    
    def fetch_events(self, category=None):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        if category:
            query = "SELECT * FROM events WHERE category = ?"
            cursor.execute(query, (category, ))
        else:
            query = "SELECT * FROM events LIMIT 10"
            cursor.execute(query)

        events = cursor.fetchall()

        conn.close()
        if events:
            return events
        else:
            return "No events found."
    def fetch_guest_list(self, event_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = "SELECT sold_tickets.guest_id, users.first_name, users.last_name, users.username, users.email FROM sold_tickets JOIN users ON sold_tickets.guest_id = users.id WHERE sold_tickets.event_id = ?"
        cursor.execute(query, (event_id, ))

        event_guests = cursor.fetchall()

        conn.close()
        if event_guests:
            event_guest_objects = []
            for guest_data in event_guests:
                guest_id, first_name, last_name, username, email = guest_data
                event_guest_object = EventGuest(event_id, guest_id, first_name, last_name, username, email)
                event_guest_objects.append(event_guest_object)
            
            return event_guest_objects
        else:
            return []   
    
    def send_message(self, message):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        sql_query = """
        INSERT INTO messages (sender_id, sender_email, receiver_id, receiver_name, receiver_username, title, content, message_status, sent_on)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(sql_query, (
            message.sender_id,
            message.sender_email,
            message.receiver_id,
            message.receiver_name,
            message.receiver_username,
            message.title,
            message.content,
            message.message_status,
            message.sent_on
        ))

        conn.commit()
        conn.close()
    
   
    

        
        
    
