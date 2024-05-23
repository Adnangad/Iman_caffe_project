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
    
    return jsonify({'message': 'Item added to cart successfully', 'cart': cart_item.to_dict()}), 200

@app.route('/remove_item/<cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    cart = storage.get(Cart, cart_id)
    if cart is None:
        return jsonify({'message': 'Not found'}), 400
    storage.delete(cart)
    
    storage.save()
    return jsonify({}), 200
@app.route("/menu")
def get_menu():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    stocks = sorted(list(storage.all(Stock).values()), key=lambda x: x.product)
    user_id = session['user_id']
    user = storage.get(User, user_id)
    user_dict = user.to_dict() if user else None
    return render_template('menu.html', stocks=stocks, cache_id=cache_id, user=user_dict)

@app.route("/users/<user_id>/carts", methods=['GET'])
def get_cart(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(400, 'No user found')
    carts = [cart.to_dict() for cart in user.carts]
    return jsonify(carts), 200

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
    storage.reload()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
