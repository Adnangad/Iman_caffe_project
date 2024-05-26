from models.stock import Stock
from models import storage
import os

stock = Stock(product='chips', value=200, description='A plate of chips', image='images/chips.jpg', category='Foods')
storage.new(stock)
storage.save()