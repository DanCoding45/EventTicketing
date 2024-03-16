from flask import Blueprint, jsonify, request, redirect, url_for, session, render_template, flash
from flask_cors import CORS 
from .models import Cart, Ticket 
from .forms import AddToCartForm, RemoveFromCartForm, ClearCartForm

app = Flask(__name__)
CORS(app)

# Sample shopping cart data and quantity
cart_items = {
    'ticket1': 1,
    'ticket2': 1,
    'ticket3': 3
}

# Sample ticket and price
def calculate_total_price():
    prices = {
        'ticket1': 100.00,
        'ticket2': 125.00,
        'ticket3': 50.00
    }
    total_price = sum(prices[item] * quantity for item, quantity in cart_items.items())
    return round(total_price, 2)

shopping_cart = Blueprint("shopping_cart", __name__)

@shopping_cart.route('/cart', methods=["GET", "POST"])
def cart():
    if not current_user.is_authenticated:
        flash('You need to login to view your cart', category='danger')
        return redirect(url_for('auth.login'))

    total_price = calculate_total_price()
    user_id = current_user.id 
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    tickets = []
    final_total = 0
    for item in cart_items:
        ticket = Ticket.query.get(item.ticket_id)
        ticket.quantity = item.quantity
        final_total += ticket.price * ticket.quantity
        tickets.append(ticket)
    return render_template('cart.html', cart=tickets, final_total=final_total)

@shopping_cart.route('/add_to_cart', methods=["GET", "POST"])
def add_to_cart():
    if not current_user.is_authenticated:
        flash('You need to login to add items to your cart', category='danger')
        return redirect(url_for('auth.login'))

    data = request.json
    ticket_id = data['ticket_id']
    user_id = current_user.id 
    cart_item = Cart.query.filter_by(ticket_id=ticket_id, user_id=user_id).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save_to_db() 
    else:
        cart = Cart(ticket_id=ticket_id, user_id=user_id, quantity=1)
        cart.save_to_db()  
    return jsonify({"message": "Added to cart"})

@shopping_cart.route('/remove_from_cart/<int:ticket_id>/remove', methods=["GET", "POST"])
def remove_from_cart(ticket_id):
    if not current_user.is_authenticated:
        flash('You need to login to remove items from your cart', category='danger')
        return redirect(url_for('auth.login'))

    user_id = current_user.id 
    cart_item = Cart.query.filter_by(ticket_id=ticket_id, user_id=user_id).first()

    if not cart_item:
        flash('Item not found in cart', category='danger')
        return redirect(url_for('shopping_cart.cart'))

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save_to_db()  
    else:
        cart_item.delete_from_db()  

    return redirect(url_for('shopping_cart.cart'))

@app.route('/cart/clear', methods=["GET", "POST"])
def clear_cart():
    if not current_user.is_authenticated:
        flash('You need to login to access your cart', category='danger')
        return redirect(url_for('auth.login'))

    user_id = current_user.id
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    for cart_item in cart_items:
        cart_item.delete_from_db()

    return redirect(url_for('shopping_cart.cart'))

app.register_blueprint(shopping_cart)

