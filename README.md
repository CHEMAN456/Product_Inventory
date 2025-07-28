# Product_Inventory

Login as a superuser(Test API endpoints after authentication)
Username - cheta
Password - superuser

## 🚀 Features

- ✅ Add and list products (with SKU and unit price)
- 🔄 Record stock IN and OUT transactions
- 📦 Track stock levels for each product
- 👤 Basic user authentication (login/logout)
- 📊 View transaction history
- 🔌 REST API for products and transactions (GET/POST)
- 🎨 Clean UI using Bootstrap 5

## 📂 Tech Stack

- Python 
- Django 
- Django REST Framework
- Bootstrap 5
- PostgreSQL
- Render (deployment)

## 📁 Database Schema

- `ProdMast`: Stores product data (`prod_name`, `sku`, `unit_price`)
- `StckMain`: Records each stock transaction (`IN/OUT`, timestamp, reference number, etc.)
- `StckDetail`: Contains product & quantity for each transaction

## 🧪 API Endpoints(tested via Postman)

- `GET /api/products/` – List products
- `POST /api/products/` – Add product
- `GET /api/transactions/` – List transactions
- `POST /api/transactions/` – Create transaction

## ✅ Validations

- Prevents OUT transactions if stock is insufficient
- All form inputs validated using Django Forms and DRF serializers
- Proper HTTP status codes and error messages returned via API

## 📦 How to Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/Product_Inventory.git
cd Product_Inventory
python -m venv env
source env/bin/activate  # Or `env\Scripts\activate` on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
