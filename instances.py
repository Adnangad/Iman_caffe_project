from models.user import User
from models import storage
user = User(name='Gard', email='adnanobuya@gmail.com', password='ndozi', location='Kisumu')
storage.new(user)
storage.save()