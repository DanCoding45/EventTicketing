from flask import Blueprint, jsonify, request, redirect, url_for, session, render_template, flash
from .models import Ticket 
from .forms import AddToCartForm, RemoveFromCartForm, ClearCartForm

shopping_cart = Blueprint("shopping_cart", __name__)


@shopping_cart.route('/cart', methods=["GET", "POST"])
def cart():
    if not session["logged_in"]:
        flash('You need to login to view your cart', category='danger')
        return redirect(url_for('auth.login'))
    return render_template('cart.html')

@shopping_cart.route('/add_to_cart', methods=["GET", "POST"])
def add_to_cart():
    
    form = AddToCartForm()
    if request.method == "POST":
    
        if not session.get("logged_in"):
            flash('You need to login to add items to your cart', category='danger')
            return redirect(url_for('auth.login'))
        
        # store shopping_cart as hashmap in session
        if "shopping_cart" not in session:
            session["shopping_cart"] = {"items": {}, "total_price": 0.00}

        # get data from form
        event_id = request.form.get("event_id")
        event_name = request.form.get("event_name")
        city = request.form.get("city")
        state = request.form.get("state")
        venue = request.form.get("venue")
        date = request.form.get("date")
        ticket_price = float(request.form.get("price")) 
        ticket_quantity = int(form.quantity.data)

        # Check if the ticket is already in the shopping cart
        if event_id in session["shopping_cart"]["items"]:
            flash("Item already in cart", category="danger")
            return redirect(url_for('event_guest.home'))

        # Add new item to the shopping cart
        new_item = {"price": ticket_price, "quantity": ticket_quantity, "event_id": event_id, "event_name": event_name, "city": city, "state": state, "venue": venue, "date": date}
        session["shopping_cart"]["items"][event_id] = new_item
        session["shopping_cart"]["total_price"] += (ticket_price * ticket_quantity)

        flash("Item added to cart", category="success")

        return redirect(url_for('event_guest.home'))


@shopping_cart.route('/remove_from_cart/<string:ticket_id>/remove', methods=["GET", "POST"])
def remove_from_cart(ticket_id):
    if not session["logged_in"]:
        flash('You need to login to remove items from your cart', category='danger')
        return redirect(url_for('auth.login'))

    print(session["shopping_cart"]["items"].keys())
    
    if "shopping_cart" not in session:
        flash('Your shopping cart is empty', category='danger')
        return redirect(url_for('event_guest.home'))

    if ticket_id not in session["shopping_cart"]["items"]:
        flash('Item not found in your cart', category='danger')
        return redirect(url_for('event_guest.home'))

    # Retrieve ticket details
    ticket = session["shopping_cart"]["items"][ticket_id]
    ticket_price = ticket["price"]
    ticket_quantity = ticket["quantity"]

    # Update total price
    session["shopping_cart"]["total_price"] -= (ticket_price * ticket_quantity)

    # Remove item from the shopping cart
    del session["shopping_cart"]["items"][ticket_id]

    flash('Item removed from your cart', category='success')
    print(session["shopping_cart"])
    return render_template('cart.html')
    
@shopping_cart.route('/cart/clear', methods=["GET", "POST"])
def clear_cart():
    if not session.get("logged_in"):
        flash('You need to login to view your cart', category='danger')
        return redirect(url_for('auth.login'))

    if "shopping_cart" in session:
        # Clear the items from the shopping cart
        session["shopping_cart"]["items"] = {}
        # Reset the total price
        session["shopping_cart"]["total_price"] = 0.00
        flash('Your cart has been cleared', category='success')
    else:
        flash('Your shopping cart is already empty', category='warning')

    return render_template('cart.html')

@shopping_cart.route('/cart/checkout', methods=["GET", "POST"])
def checkout():
    if not session["logged_in"]:
        flash('You need to login to view your cart', category='danger')
        return redirect(url_for('auth.login'))
    return render_template('checkout.html')


