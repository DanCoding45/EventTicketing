from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from .services import EventManagerServices
from .models import Message

event_manager = Blueprint("event_manager", __name__)

event_manager_services = EventManagerServices()


@event_manager.route('/manager/home/<string:category>')
@event_manager.route('/manager/home', defaults={"category": 'sports'})
def home(category):
    events = []
    if category:
        events=event_manager_services.fetch_events(category.capitalize())
    else:
        events=event_manager_services.fetch_events()
    
    return render_template('dashboards/event_manager_dashboard.html', events=events)

@event_manager.route('/manager/guest_list/<string:event_id>')
def guest_list(event_id):
    event_guests = event_manager_services.fetch_guest_list(event_id)
    if event_guests:  # Check if event_guests is not empty
        print(event_guests)
        return render_template('notifications/event_guest_list.html', event_id=event_id, event_guests=event_guests)
    else:
        return render_template('notifications/event_guest_list.html', event_id=event_id)

@event_manager.route('/manager/send_message', methods=["GET", "POST"])
def send_message():
    
    if request.method == "POST":
        title = request.form.get('title')
        message = request.form.get('message')
        user_id = request.form.get('user_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        
        message = Message(
            sender_id=session['host_id'],
            sender_email=session["host_email"],
            receiver_id=user_id,
            receiver_name=f"{first_name} {last_name}",
            receiver_username=username,
            title=title,
            content=message,
        )
        
        event_manager_services.send_message(message)
        
    return redirect(url_for("event_manager.home"))
