# Bose Service Center – Service Booking Platform

> ⚠️ **Note:** The original production website is currently offline due to organizational changes at the company. The application remains fully functional and can be redeployed on request. A GitHub Pages preview/demo link will be added below.

A production-grade service booking platform built with Django for managing customer service requests, online payments, order processing, and administrative operations.

The platform successfully processed **500+ customer bookings during its first quarter in production** with **zero critical payment failures**, ensuring a reliable booking and payment experience.

---

## Screenshots

<img width="1919" height="956" alt="Home Page" src="https://github.com/user-attachments/assets/1b1fdf83-5ec7-40f8-9a53-1c57744513a3" />

<img width="1920" height="959" alt="Booking Page" src="https://github.com/user-attachments/assets/86a26c75-d46e-423b-8a3f-9f5ec014c733" />

<img width="1920" height="1000" alt="Dashboard" src="https://github.com/user-attachments/assets/afca2932-efcd-42b2-859b-f17966e2f5e7" />

---

# Tech Stack

## Backend

- Python
- Django

## Database

- MySQL

## Frontend

- HTML
- CSS
- JavaScript

## Payment Gateway

- Cashfree Payments

## Deployment

- Linux VPS
- Gunicorn
- Nginx

---

# Key Features

- Customer service booking system
- Secure online payment integration using Cashfree
- Real-time booking confirmation
- Order lifecycle management
- Custom admin dashboard
- Customer and order management
- Inventory management
- Email notifications for customers
- Authentication and authorization
- Responsive user interface
- Production deployment with Gunicorn and Nginx

---

# Project Highlights

- Successfully handled **500+ real customer bookings**
- Zero critical payment failures in production
- Secure payment workflow
- Custom Django admin for business operations
- Production-ready deployment on Linux VPS
- Optimized database queries for better performance

---

# Live Website

> ⚠️ The original production domain (`boseservicecenter.co.in`) is currently unavailable due to company-side changes and is no longer under my control.

**Demo / Preview**

GitHub Pages: **Add your GitHub Pages link here**

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/bose-service-center.git
```

Go to the project directory

```bash
cd bose-service-center
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure the database in `settings.py`.

Run migrations

```bash
python manage.py migrate
```

Create a superuser

```bash
python manage.py createsuperuser
```

Start the development server

```bash
python manage.py runserver
```

Open your browser

```
http://127.0.0.1:8000/
```

---



---

# License

This project is intended for portfolio and educational purposes.
