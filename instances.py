"""
This module adds items to the database for consumers to choose.
"""
from models.stock import Stock
from models import storage

from models.stock import Stock
from models import storage
from models.area import Area
import os

stock1 = Stock(product='Beef_stew', value=150, description='A plate of beef stew', image='images/beef_stew.jpg', category='Foods')
stock2 = Stock(product='Biriani', value=250, description='A plate of biriani', image='images/biriani.jpg', category='Foods')
stock3 = Stock(product='Chapati', value=70, description='2 rolls of chapatis', image='images/chapati.jpg', category='Foods')
stock4 = Stock(product='Chicken', value=200, description='3 pieces of chicken', image='images/chicken.jpg', category='Foods')
stock5 = Stock(product='Coffee', value=50, description='A cup of coffee', image='images/cofee.jpg', category='Beverages')
stock6 = Stock(product='Chips', value=175, description='A plate of chips', image='images/chips.jpg', category='Foods')
stock7 = Stock(product='Fish', value=100, description='1 fried fish', image='images/fish.jpg', category='Foods')
stock8 = Stock(product='Githeri', value=75, description='A plate of githeri', image='images/githeri.jpg', category='Foods')
stock9 = Stock(product='Hamburger', value=100, description='One burger', image='images/hamburger.jpg', category='Foods')
stock10 = Stock(product='Lemon tea', value=50, description='A cup of lemon tea', image='images/lemon_tea.jpg', category='Beverages')
stock11 = Stock(product='Mango Juice', value=75, description='A glass of mango juice', image='images/mixed_juice.jpg', category='Drinks')
stock12 = Stock(product='Nyama Choma', value=200, description='A plate of nyama choma', image='images/nyama.jpg', category='Foods')
stock13 = Stock(product='Orange Juice', value=75, description='A glass of orange juice', image='images/orange_juice.jpg', category='Drinks')
stock14 = Stock(product='Pilau', value=200, description='A plate of pilau', image='images/pilau.jpg', category='Foods')
stock15 = Stock(product='Samosas', value=50, description='1 meat samosa', image='images/samosa.jpg', category='Foods')
stock16 = Stock(product='Sausages', value=60, description='2 sausages', image='images/sausage.jpg', category='Foods')
stock17 = Stock(product='Tea', value=50, description='A cup of tea', image='images/tea.jpg', category='Beverages')
stock18 = Stock(product='Ugali', value=40, description='A plate of plain ugali', image='images/ugali.jpg', category='Foods')
stock19 = Stock(product='Water', value=65, description='A bottle of water', image='images/water.jpg', category='Drinks')

stocks = sorted(list(storage.all(Stock).values()), key=lambda x: x.product)
seen_products = set()
stocks_to_delete = []

for stock in stocks:
    if stock.product in seen_products:
        stocks_to_delete.append(stock)
    else:
        seen_products.add(stock.product)


for stock in stocks_to_delete:
    storage.delete(stock)

storage.save()
