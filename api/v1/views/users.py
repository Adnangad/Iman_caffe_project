from flask import *
from models.user import User
from models import storage
from api.v1.views import app_views

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    user = request.get_json()
    if not 'user':
        abort(400, 'Not a JSON')
    if 'name' not in user:
        abort(400, 'No username')
    if 'password' not in user:
        abort(400, 'No password')
    if 'location' not in user:
        abort(400, 'No location')
    if 'password' not in user:
        abort(400, 'No password')
    if 'email' not in user:
        abort(400, 'No email')
    new_user = User(**user)
    storage.new(new_user)
    
    storage.save()
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['UPDATE'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if not 'user':
        abort(400)
    data = request.get_json()
    if not data:
        abort(400, "not a json")
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(400, 'User not found')
    storage.delete(user)
    storage.save()
    return jsonify({}), 200