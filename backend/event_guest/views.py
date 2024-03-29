from flask import Blueprint, render_template, redirect, request, url_for, session
from .services.notification_services import EventGuestNotificationServices
from .services.event_access_services import EventAccessServices
from .models import Event
from shopping_cart.forms import AddToCartForm

event_guest = Blueprint("event_guest", __name__)

# service class used to interact with messages table on db.
event_guest_notification_services = EventGuestNotificationServices()
# service class used to interact with events table on db.
event_access_services = EventAccessServices()


@event_guest.route('/home/<string:category>')
@event_guest.route('/home', defaults={"category": None})
def home(category):
    add_to_cart_form = AddToCartForm()
    
    if category:
        fetched_events = event_access_services.get_events(category.capitalize())
    else:
        fetched_events = event_access_services.get_events()
    
    events = []
    for fetched_event in fetched_events:
        event = Event(
        id=fetched_event[0],
        name=fetched_event[1],
        category=fetched_event[2], 
        date=fetched_event[3], 
        time=fetched_event[4], 
        city=fetched_event[5], 
        state=fetched_event[6],
        country=fetched_event[7], 
        venue_name=fetched_event[8],
        image_url=fetched_event[9]
    )
        events.append(event)
        
    return render_template("dashboard.html", events=events, form=add_to_cart_form)


@event_guest.route('/notifications')
def check_notifications():
    print(session['user_id'])
    # function to check for any incoming messages
    unread_messages = event_guest_notification_services.get_unread_notifications(session["user_id"])
    return render_template("user_notifications.html", unread_messages=unread_messages)


@event_guest.route('/update_message_status', methods=["POST"])
def update_message_status():
    # function to toggle message status
    if request.method == "POST":
        message_id = request.form.get('message_id')
        event_guest_notification_services.update_message_status(message_id)

    return redirect(url_for("event_guest.check_notifications"))
