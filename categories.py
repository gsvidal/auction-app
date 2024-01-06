# exec(open('categories.py').read())
from auctions.models import Category

art = Category(name="Art")
art.save()

electronics = Category(name="Electronics")
electronics.save()

fashion = Category(name="Fashion")
fashion.save()

home = Category(name="Home")
home.save()

vehicles = Category(name="Vehicles")
vehicles.save()
