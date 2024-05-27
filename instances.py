from models.stock import Stock
from models import storage

# Retrieve and sort all Stock items by their product attribute
stocks = sorted(list(storage.all(Stock).values()), key=lambda x: x.product)

# Set to keep track of products we've seen
seen_products = set()

# List to keep track of stocks to be deleted
stocks_to_delete = []

for stock in stocks:
    if stock.product in seen_products:
        # If product is already seen, mark stock for deletion
        stocks_to_delete.append(stock)
    else:
        # Otherwise, add product to seen_products
        seen_products.add(stock.product)

# Delete the marked stocks
for stock in stocks_to_delete:
    storage.delete(stock)

# Save changes to storage
storage.save()
