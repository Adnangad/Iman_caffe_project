from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from models.user import User
from models import storage
from models.area import Area
from models.stock import Stock
from models.cart import Cart
from uuid import uuid4
import os
from collections import defaultdict
import requests
from requests.auth import HTTPBasicAuth
import datetime
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management
cache_id = uuid4()
base_url = 'https://imaan-caffe-f7f987595df4.herokuapp.com/cart'
consumer_key = 'S3a3NAoXyGasPf40g4dULSJur3wGsPvRiMzhu29zj5QAUCw6'
consumer_secret = 'fPDIgXr6kVvhaZ2Ayu5EMeXXeJRvKLim3G8wqr2lwFA2jSCsDJGYw05VLkgxSmA2'

@app.route('/access_token')
def get_access_token():
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data['access_token']

def _access_token():
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data['access_token']

@app.route('/register')
def register_urls():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    access_token = _access_token()
    my_endpoint = base_url + "/c2b/"
    headers = { "Authorization": "Bearer %s" % access_token }
    r_data = {
        "ShortCode": "600383",
        "ResponseType": "Completed",
        "ConfirmationURL": my_endpoint + 'con',
        "ValidationURL": my_endpoint + 'val'
    }
    response = requests.post(endpoint, json=r_data, headers=headers)
    return response.json()

@app.route('/simulate')
def test_payment():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    access_token = _access_token()
    headers = { "Authorization": "Bearer %s" % access_token }
    data_s = {
        "Amount": 100,
        "ShortCode": "600383",
        "BillRefNumber": "test",
        "CommandID": "CustomerPayBillOnline",
        "Msisdn": "254708374149"
    }
    res = requests.post(endpoint, json=data_s, headers=headers)
    return res.json()

@app.route('/b2c')
def make_payment():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
    access_token = _access_token()
    headers = { "Authorization": "Bearer %s" % access_token }
    my_endpoint = base_url + "/b2c/"
    data = {
        "InitiatorName": "apitest342",
        "SecurityCredential": "YourSecurityCredentialHere",
        "CommandID": "BusinessPayment",
        "Amount": "200",
        "PartyA": "601342",
        "PartyB": "254708374149",
        "Remarks": "Pay Salary",
        "QueueTimeOutURL": my_endpoint + "timeout",
        "ResultURL": my_endpoint + "result",
        "Occasion": "Salary"
    }
    res = requests.post(endpoint, json=data, headers=headers)
    return res.json()

@app.route('/lnmo')
def init_stk():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    access_token = _access_token()
    headers = { "Authorization": "Bearer %s" % access_token }
    my_endpoint = base_url + "/lnmo"
    Timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + Timestamp
    datapass = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    data = {
        "BusinessShortCode": "174379",
        "Password": datapass,
        "Timestamp": Timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": "YourPhoneNumber",
        "PartyB": "174379",
        "PhoneNumber": "YourPhoneNumber",
        "CallBackURL": my_endpoint,
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": 2
    }
    res = requests.post(endpoint, json=data, headers=headers)
    return res.json()

@app.route('/lnmo', methods=['POST'])
def lnmo_result():
    data = request.get_data()
    with open('lnmo.json', 'a') as f:
        f.write(data.decode('utf-8'))
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

@app.route('/b2c/result', methods=['POST'])
def result_b2c():
    data = request.get_data()
    with open('b2c.json', 'a') as f:
        f.write(data.decode('utf-8'))
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

@app.route('/b2c/timeout', methods=['POST'])
def b2c_timeout():
    data = request.get_json()
    with open('b2ctimeout.json', 'a') as f:
        f.write(data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

@app.route('/c2b/val', methods=['POST'])
def validate():
    data = request.get_data()
    with open('data_v.json', 'a') as f:
        f.write(data.decode('utf-8'))
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

@app.route('/c2b/con', methods=['POST'])
def confirm():
    data = request.get_json()
    with open('data_c.json', 'a') as f:
        f.write(data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

@app.route("/", strict_slashes=False)
def index():
    return render_template("index.html", cache_id=cache_id)

@app.route("/location", methods=['POST'])
def check_Area():
    area = storage.all(Area).values()
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Please enter a valid location'}), 400
    loc = data.get('area')
    for a in area:
        if loc == a.name:
            return jsonify({'message': 'We do deliver in that location'}), 200
    return jsonify({'message': 'Sorry but we are not yet available in that location'}), 400

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
            return jsonify({'message': 'Email Address already exists.'}), 400
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
    cart_item = Cart(user_id=user.id, item=data['item'], price=data['price'], image=data['image'])
    storage.new(cart_item)
    storage.save()
    number_of_items = sum(1 for cart in storage.all(Cart).values() if cart.user_id == user_id and cart.item == cart_item.item)
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
    number_of_items = sum(1 for cart in carts if cart.user_id == user.id and cart.id == cart_id)
    return jsonify({'message': 'Item removed from cart successfully', 'number_of_items': number_of_items}), 200

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
    stocks = sorted(list(storage.all(Stock).values()), key=lambda x: x.product)
    if 'user_id' not in session:
        return render_template('item.html', stock=stock)
    user_id = session['user_id']
    user = storage.get(User, user_id)
    return render_template('item.html', stock=stock, user=user, stocks=stocks)

@app.route("/cart", methods=["GET"])
def show_cart():
    if 'user_id' not in session:
        return jsonify({'message': 'Please login.'}), 401
    user_id = session['user_id']
    user = storage.get(User, user_id)
    carts = sorted(list(storage.all(Cart).values()), key=lambda x: x.item)
    grouped_carts = defaultdict(lambda: {'count': 0, 'details': {}})
    total_price = 0
    for cart in carts:
        if cart.user_id == user.id:
            item_name = cart.item
            grouped_carts[item_name]['count'] += 1
            grouped_carts[item_name]['details'] = cart
            total_price += float(cart.price)
    return render_template('cart.html', user=user, grouped_carts=grouped_carts, cache_id=cache_id, total_price=total_price)

@app.route('/user/', methods=['GET'])
def user_info():
    if 'user_id' not in session:
        return jsonify({'message': 'User does not exist'}), 400
    user_id = session['user_id']
    user = storage.get(User, user_id)
    return render_template('user.html', user=user)

@app.route('/logout', methods=['GET'])
def log_out():
    if 'user_id' not in session:
        return jsonify({'message': 'User does not exist'}), 400
    del session['user_id']
    return render_template('index.html', cache_id=cache_id)

@app.route('/payment', methods=['POST'])
def payment():
    phone = request.form['phone']
    amount = request.form['amount']
    access_token = _access_token()
    headers = {"Authorization": "Bearer %s" % access_token}
    my_endpoint = base_url + "/lnmo"
    Timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + Timestamp
    datapass = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    data = {
        "BusinessShortCode": "174379",
        "Password": datapass,
        "Timestamp": Timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": my_endpoint,
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": amount
    }
    res = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json=data, headers=headers)
    return res.json()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)