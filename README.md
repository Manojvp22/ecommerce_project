🛒 Django E-Commerce Project

A full-featured Django E-Commerce Web Application with product listing, cart management, user authentication, checkout, and Razorpay Payment Gateway integration.
Built using Python, Django, MySQL, Bootstrap, and follows clean architecture.
  
---
🚀 Features
🛍 Product Features

  *  Browse all products

  *  Product details page

  *  Add items to cart

  * Update item quantity

  *  Remove products from cart

  *  Display price, stock, subtotal

----

🧺 Cart & Checkout

  *  User-specific cart

  *  Cart total auto-calculations

  *  Simple & clean UI

  *  Checkout page with Razorpay integration

----

💳 Payment Gateway (Razorpay)

  *  Create Razorpay order via REST API

  *  Integrated Razorpay popup checkout

  *  Payment verification (signature check)

  *  Auto-clear cart on successful payment

  *  Store orders in database

----

🔐 User Authentication

  *  Login / Register / Logout

  *  Cart linked to logged-in user

  *  Secure pages using @login_required

----

🗄 Database

  *  MySQL configured

  *  Models:

    *  Product

    *  Cart

    *  CartItem

    *  Order

----

🎨 Frontend

  *  Bootstrap-based UI

  *  Navbar

  *  Product cards

  *  Clean checkout UI 

---

| Layer           | Technology            |
| --------------- | --------------------- |
| Backend         | Django 5 (Python)     |
| Frontend        | HTML, CSS, Bootstrap  |
| Database        | MySQL                 |
| Payment         | Razorpay API          |
| Auth            | Django Authentication |
| Version Control | Git & GitHub          |


---

📂 Project Structure

    ecommerce_project/
    │── ecommerce/              # Project settings
    │   ├── settings.py
    │   ├── urls.py
    │
    │── accounts/               # Login / Register
    │   ├── urls.py
    │   ├── views.py
    │
    │── products/               # E-commerce logic
    │   ├── models.py           # Product, Cart, CartItem, Order
    │   ├── views.py
    │   ├── urls.py
    │   ├── templates/products/
    │       ├── base.html
    │       ├── product_list.html
    │       ├── product_detail.html
    │       ├── cart_view.html
    │       ├── checkout.html
    │       ├── order_success.html
    │
    │── requirements.txt
    │── manage.py
    │── README.md
    │── .gitignore

    
-----

🛠 Installation & Setup

1️⃣ Clone the repository

    git clone https://github.com/Manojvp22/ecommerce_project.git
    cd ecommerce_project

2️⃣ Create virtual environment

    python -m venv venv
    venv\Scripts\activate        # Windows
    source venv/bin/activate    # Mac/Linux

3️⃣ Install dependencies

    pip install -r requirements.txt

4️⃣ Configure MySQL in settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ecommerce_db',
            'USER': 'root',
            'PASSWORD': 'YOUR_PASSWORD',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

5️⃣ Apply migrations

    python manage.py makemigrations
    python manage.py migrate

6️⃣ Create superuser

    python manage.py createsuperuser

7️⃣ Run the server

    python manage.py runserver

----

💳 Razorpay Integration

Steps:

  1.  Go to Razorpay Dashboard → https://dashboard.razorpay.com

  2.  Generate:

    RAZORPAY_KEY_ID
    RAZORPAY_KEY_SECRET

  3.  Add to settings.py:

    RAZORPAY_KEY_ID = "your_key_id"
    RAZORPAY_KEY_SECRET = "your_secret_key"

  4.  On checkout, Razorpay popup handles payment.

  5.  Payment callback verifies signature and stores order details.

----

📌 Future Enhancements

  *  Product categories

  *  Search & filtering

  *  Order history page

  *  Admin sales dashboard

  *  Email notifications

  *  REST API using DRF

  *  Product images

----

👨‍💻 Author

  Manoj V Poojar

  Python & Django Developer



  

    
    

