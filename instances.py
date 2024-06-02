from models.stock import Stock
from models import storage

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
