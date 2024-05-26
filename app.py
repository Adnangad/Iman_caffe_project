from flask import *
from models.user import User
from models import storage
from models.area import Area
from models.stock import Stock
from models.cart import Cart
from uuid import uuid4
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 
cache_id = uuid4()

@app.route("/", strict_slashes=False)
def index():
    return render_template("index.html", cache_id=cache_id)

@app.route("/location", methods=['POST'])
def check_Area():
    area = storage.all(Area).values()
    loc = request.form['area']
    if not loc:
        message = 'Please Enter a location'
        return render_template('menu.html', cache_id=cache_id, message=message)
    for a in area:
        if loc == a.name:
            return render_template('menu.html', cache_id=cache_id)
    message = "Sorry but we currently don't do deliveries in that location"
    return render_template('index.html', cache_id=cache_id, message=message)

@app.route("/login", methods=["POST"])
def sign_in():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Request must be JSON.'}), 400
    mail = data['email']
    password = data['password']
    users = storage.all(User).values()
    for user in users:
        if user.email == mail:
            real_user = storage.get(User, user.id)
            if real_user.password == password:
                session['user_id'] = real_user.id
                return jsonify({'message': 'Login successful', 'user': real_user.to_dict()}), 200
    return jsonify({'message': 'Invalid email or password.'}), 401

@app.route("/sign_up", methods=['POST'])
def sign_up():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Request must be JSON.'}), 400
    mail = data['email']
    users = storage.all(User).values()
    for user in users:
        if user.email == mail:
            return jsonify({'message': 'Email Adress already exists.'}), 400
    new_user = User(**data)
    storage.new(new_user)
    
    storage.save()
    return jsonify({'message': 'You have been successfully added to the database, you can now login', 'user': new_user.to_dict()}), 200

@app.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'message': 'Please login.'}), 401    
    user_id = session['user_id']
    user = storage.get(User, user_id)    
    if not user:
        return jsonify({'message': 'User not found. Please login again.'}), 401    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Request must be JSON.'}), 400    
    if 'item' not in data or 'price' not in data or 'image' not in data:
        return jsonify({'message': 'Missing item name, price, or image.'}), 400
    cart_item = Cart(user_id=user_id, item=data['item'], price=data['price'], image=data['image'])
    storage.new(cart_item)
    storage.save()
    number_of_items = sum(1 for cart in storage.all(Cart).values() if cart.user_id == user_id and cart.item == cart_item.item)
    number_of_items = str(number_of_items)
    return jsonify({'message': 'Item added to cart successfully', 'number_of_items': number_of_items, 'cart_item': cart_item.id}), 200

@app.route('/remove_item/<cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    cartz = storage.get(Cart, cart_id)
    if cartz is None:
        return jsonify({'message': 'Not found'}), 400
    storage.delete(cartz)    
    storage.save()
    if 'user_id' not in session:
        return jsonify({'message': 'Please login.'}), 401    
    user_id = session['user_id']
    user = storage.get(User, user_id)
    carts = sorted(list(storage.all(Cart).values()), key=lambda x: x.item)
    number_of_items = 0
    for cart in carts:
        if cart.user_id == user.id and cart.id == cart_id:
            number_of_items = number_of_items + 1
    number_of_items = str(number_of_items)
    return jsonify({'message': 'Item added to cart successfully', 'number_of_items': number_of_items}), 200
@app.route("/menu")
def get_menu():
    stocks = sorted(list(storage.all(Stock).values()), key=lambda x: x.product)
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    user = storage.get(User, user_id)
    return render_template('menu.html', stocks=stocks, cache_id=cache_id, user=user)
@app.route('/checkitem/<stock_id>')
def check_item(stock_id):
    stock = storage.get(Stock, stock_id)
    if 'user_id' not in session:
        return render_template('item.html', stock=stock)
    user_id = session['user_id']
    user = storage.get(User, user_id)
    return render_template('item.html', stock=stock, user=user)


@app.route("/cart", methods=["GET"])
def show_cart():
    if 'user_id' not in session:
        return jsonify({'message': 'Please login.'}), 401
    user_id = session['user_id']
    user = storage.get(User, user_id)
    carts = sorted(list(storage.all(Cart).values()), key=lambda x: x.item)
    final = []
    total_price = 0
    for cart in carts:
        if cart.user_id == user.id:
            total_price = total_price + float(cart.price)
            final.append(cart)
    return render_template('cart.html', user=user, carts=final, cache_id=cache_id, total_price=total_price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))