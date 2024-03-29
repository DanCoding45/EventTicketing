from datetime import date

class Message:
    def __init__(self, sender_id, sender_email, receiver_id, receiver_name, receiver_username, title, content):
        self.sender_id = sender_id
        self.sender_email = sender_email
        self.receiver_id = receiver_id
        self.receiver_name = receiver_name
        self.receiver_username = receiver_username
        self.title = title
        self.content = content
        self.sent_on = date.today()
        self.message_status = "Unread"
        
class EventGuest:
    def __init__(self, event_id, guest_id, first_name, last_name, username, email):
        self.event_id = event_id
        self.guest_id = guest_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email