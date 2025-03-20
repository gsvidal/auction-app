# Auctions App

## Introduction

Welcome to the **Auctions Django App**! This web application allows users to create, browse, and participate in online auctions. Users can list items for auction, place bids, comment on listings, and manage their watchlist.

<a href="https://auction-app-nr4r.onrender.com/" >
<img src="https://i.postimg.cc/RZF3vqCs/auctions.gif" width="800" alt="Auction application">
</a>

## Table of Contents

- [Demo](#demo)
- [Technologies](#technologies)
- [Features](#features)
- [Installation](#installation)

## 🚀 Live Demo (Currently Unavailable)
⚠️ Note: The live demo is currently offline as the database instance is not running to reduce hosting costs. However, you can still explore the full source code and set it up locally.

## Technologies
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/html5/html5-original-wordmark.svg" alt="html5 Logo" width="50" height="50"/><img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/css3/css3-original-wordmark.svg" alt="css3 Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/javascript/javascript-original.svg" alt="Javascript Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/python/python-original-wordmark.svg" alt="Python Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/django/django-plain-wordmark.svg" alt="Django Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/postgresql/postgresql-original-wordmark.svg" alt="Python Logo" width="50" height="50"/>

## Deployment
Deployed and hosted as a web service in <img src="https://ptimofeev.com/images/render.png" alt="Render Logo" width="125" height="25"/>

## Features
**User Authentication:**

Users can register, log in, and log out.
Passwords are securely hashed for user authentication.

**Listings:**

Users can create new auction listings.
Each listing includes a title, description, starting bid, image URL, and category.

**Bidding:**

Users can place bids on active listings.
The highest bid is displayed on each listing.

**Watchlist:**

Users can add listings to their watchlist.
Watchlist items are easily accessible for users to keep track of.

**Comments:**

Users can comment on listings to share information or ask questions.

**Categories:**

Listings can be categorized, and users can browse listings by category.

**Winner Notification:**

When a listing is closed, the winner is notified.

## Installation
### Clone the Repository:
`git clone git@github.com:gsvidal/auction-app.git`

### Create a Virtual Environment:
`python -m venv venv`

###Activate the Virtual Environment:
#### On Windows:
`venv\Scripts\activate`

#### On macOS/Linux:
`source venv/bin/activate`

### Install Dependencies:
`pip install -r requirements.txt`

### Run Migrations:
`python manage.py migrate`

### Create Superuser (Optional):
`python manage.py createsuperuser`

### Run the Development Server:
`python manage.py runserver`

### Access the Application:
Open your web browser and go to http://localhost:8000
