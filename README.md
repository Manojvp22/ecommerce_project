# Django E-Commerce Project

A Django-based e-commerce web application with product browsing, product images, user authentication, cart management, Razorpay checkout, and order handling.

Live demo: https://your-render-app-name.onrender.com

## Features

### Products

- Product listing with images, prices, stock, and descriptions
- Vertical product list layout
- Product detail page
- Seeded sample products with local media images
- Admin support for managing product images

### Cart

- User-specific cart
- Add products to cart
- Quantity increases automatically when the same product is added again
- Quantity changes auto-save from the cart page
- Remove items from cart
- Automatic subtotal and cart total calculation

### Checkout And Payment

- Checkout summary page
- Razorpay popup checkout integration
- Razorpay order creation
- Payment signature verification
- Order status tracking
- Cart clears after successful payment

### Authentication

- Login
- Register with email
- Logout
- Forgot password flow
- Password reset pages
- Show/hide password eye button on password fields

### UI

- Bootstrap-based responsive layout
- Updated product list, product detail, cart, checkout, login, register, and password reset pages
- Cleaner color theme
- Product images display without cropping

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Django 5, Python |
| Frontend | HTML, CSS, Bootstrap |
| Local Database | MySQL |
| Production Database | PostgreSQL |
| Payment | Razorpay |
| Auth | Django Authentication |
| Deployment | Render |
| Version Control | Git, GitHub |

## Project Structure

```text
ecommerce_project/
├── accounts/
│   ├── forms.py
│   ├── urls.py
│   ├── views.py
│   └── templates/accounts/
├── ecommerce/
│   ├── settings.py
│   └── urls.py
├── media/products/
├── products/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── templates/products/
├── manage.py
├── requirements.txt
└── README.md
```

## Local Setup

1. Clone the repository:

```powershell
git clone https://github.com/Manojvp22/ecommerce_project.git
cd ecommerce_project
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Configure environment variables in `.env`:

```env
ENVIRONMENT=local
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

5. Apply migrations:

```powershell
python manage.py migrate
```

6. Create a superuser:

```powershell
python manage.py createsuperuser
```

7. Run the server:

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Razorpay Test Mode

The app supports Razorpay checkout. For local testing, use Razorpay test keys from the Razorpay dashboard.

In test mode, use Razorpay test payment details inside the Razorpay popup. Do not scan a real QR code with test keys.

## Important Commands

```powershell
python manage.py check
python manage.py migrate
python manage.py runserver
python -m pip freeze > requirements.txt
```

## Deployment

The project is prepared for Render deployment with:

- PostgreSQL support in production
- Environment variable support
- WhiteNoise static file serving
- GitHub-based deployment flow

## Future Enhancements

- Product search
- Product categories
- Order history page
- Admin sales dashboard
- Email notifications
- Cloud media storage using Cloudinary or S3
- REST API using Django REST Framework

## Author

Manoj V Poojar

Python and Django Developer
