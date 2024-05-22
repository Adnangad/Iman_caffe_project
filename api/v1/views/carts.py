from models.cart import Cart
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/users/<user_id>/carts', methods=['GET'], strict_slashes=False)
def get_cart(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(400, 'No user found')
    carts = [cart.to_dict() for cart in user.carts]
    return jsonify(carts), 200

@app_views.route('/users/<user_id>/carts', methods=['POST'], strict_slashes=False)
def create_new_cart(user_id):
    """creates an instance of an item and adds it to the database"""
    user = storage.get(User, user_id)
    if not user:
        abort(404, 'user dont exist')
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'item' not in data:
        abort(400, "Missing name")
    if 'price' not in data:
        abort(400, 'missing price')
    data['user_id'] = user_id
    cart = Cart(**data)
    storage.new(cart)
    
    storage.save()
    return jsonify(cart.to_dict()), 201

@app_views.route('/carts/<cart_id>', methods=['UPDATE'], strict_slashes=False)
def update_cart(cart_id):
    cart = storage.get(Cart, cart_id)
    if cart is None:
        abort(400, 'Not found')
    data = request.get_json()
    if data is None:
        abort(400, "Not a valid JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(cart, key, value)
    cart.save()
    return jsonify(cart.to_dict()), 200


@app_views.route('/carts/<cart_id>', methods=['DELETE'], strict_slashes=False)
def delete_cart(cart_id):
    cart = storage.get(Cart, cart_id)
    if cart is None:
        abort(400, 'Not found')
    storage.delete(cart)
    storage.save()
    return jsonify({}), 200