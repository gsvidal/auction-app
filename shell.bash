# Script to run back development server

cd .venv/
source ./Scripts/activate && cd ..
python manage.py runserver


# Create product categories (sql)

from auctions.models import AuctionListing, User, Category

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


# Postgres

INSERT INTO auctions_category (name) VALUES
('Electronics'),
('Fashion'),
('Grocery'),
('Books'),
('Music'),
('Sports'),
('Games'),
('No Category');

INSERT INTO auctions_category (name) VALUES
('Home'),
('Vehicles'),
('Art');
