# Rasoi Restaurant — Table Ordering System (Django)

A full-stack Django web application for modern restaurant dining. Guests browse the curated menu, customize dishes, add to cart, and order straight to their table number. Orders flow into the live **Kitchen Display System (KDS)** and can be tracked in real-time.

---

## 🌟 Key Features

1. **Digital Menu & Discovery (`/`)**:
   - Categorized browsing: Starters, Mains, Biryani & Rice, Breads, Desserts, Drinks.
   - Live dish search and dietary filters (Veg / Non-Veg / Spicy).
   - Instant "Add to Cart" with AJAX quantity counter and floating feedback toast.
2. **Table Cart & Checkout (`/cart/`)**:
   - Session-backed persistent cart.
   - Dynamic Table selection (Table 1 through 20).
   - Special chef/kitchen preparation notes.
   - 3% restaurant tax calculation with transparent checkout summary.
3. **Live Order Tracking (`/track/` and `/track/<order_code>/`)**:
   - Unique order reference code generated per order (e.g. `RSO-A7B8C`).
   - 4-stage animated timeline:
     1. **Order Received**
     2. **In Kitchen**
     3. **Ready to Serve**
     4. **Served at Table**
   - Real-time client polling that updates the screen automatically when the kitchen changes the status.
4. **Kitchen Display System (KDS) (`/kitchen/`)**:
   - Real-time ticket board organized by table and arrival time.
   - Clear ticket badges, guest instructions, and item quantities.
   - One-click workflow buttons: `Start Preparing` ➔ `Mark Ready to Serve` ➔ `Complete / Served`.
   - Auto-refreshes every 8 seconds.
5. **Django Admin (`/admin/`)**:
   - Manage categories, menu items, prices, dietary tags, and live orders.

---

## 📁 Project Directory Structure

```text
restaruent_ordering/
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
│
├── config/                     # Core Project Configuration
│   ├── __init__.py
│   ├── settings.py             # Apps, Templates, Static, Cart Context Processor
│   ├── urls.py                 # Top-level URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── menu/                       # Menu & Catalog App
│   ├── admin.py                # Admin registration for Category & MenuItem
│   ├── apps.py
│   ├── models.py               # Category & MenuItem models
│   ├── urls.py                 # Menu routes (/ and /api/dish/<id>/)
│   ├── views.py                # Menu listing, search & filtering views
│   └── management/
│       └── commands/
│           └── seed_menu.py    # Command to seed 15+ dishes & 6 categories
│
├── orders/                     # Orders & Cart App
│   ├── admin.py                # Order & OrderItem admin with inline items
│   ├── apps.py
│   ├── cart.py                 # Session cart manager with tax & totals
│   ├── context_processors.py   # Global cart_count provider for navbar badge
│   ├── models.py               # Order (with status lifecycle) & OrderItem
│   ├── urls.py                 # /cart/, /checkout/, /track/, /api/status/
│   └── views.py                # Cart actions, checkout & tracking logic
│
├── kitchen/                    # Kitchen Display System (KDS) App
│   ├── apps.py
│   ├── urls.py                 # /kitchen/, /kitchen/update/, /kitchen/api/
│   └── views.py                # KDS ticket board & status transition API
│
├── templates/                  # Frontend HTML Templates
│   ├── base.html               # Luxury navbar, sticky header & footer
│   ├── menu/
│   │   └── index.html          # Hero banner, category chips, dish cards
│   ├── orders/
│   │   ├── cart.html           # Table selection & checkout breakdown
│   │   └── track.html          # Order tracking & animated timeline
│   └── kitchen/
│       └── display.html        # Live KDS board for chefs
│
└── static/                     # Static Assets
    ├── css/
    │   └── style.css           # Custom design system (Fraunces & Manrope fonts)
    └── js/
        └── main.js             # AJAX cart, live tracking polling & KDS updates
```

---

## 🚀 How to Run Locally

### 1. Run Migrations & Seed Menu
```bash
python manage.py migrate
python manage.py seed_menu
```

### 2. (Optional) Create an Admin Superuser
```bash
python manage.py createsuperuser
```

### 3. Start the Development Server
```bash
python manage.py runserver
```

Now open your browser:
- **Menu & Table Ordering:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Your Cart:** [http://127.0.0.1:8000/cart/](http://127.0.0.1:8000/cart/)
- **Track Order:** [http://127.0.0.1:8000/track/](http://127.0.0.1:8000/track/)
- **Kitchen Display (KDS):** [http://127.0.0.1:8000/kitchen/](http://127.0.0.1:8000/kitchen/)
- **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
