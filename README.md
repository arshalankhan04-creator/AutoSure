# Car Service Management & POS System

A complete automotive service management and point-of-sale system built with Python, Streamlit, and PostgreSQL.

## Features

- **Customer Management**: Track customers, vehicles, and service history
- **Service Orders**: Create and manage service orders with status tracking
- **Inventory Management**: Parts inventory with low-stock alerts
- **Point of Sale**: Quick sales interface for over-the-counter transactions
- **Invoicing**: Generate invoices and track payments
- **Reporting**: Business analytics and reports

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: PostgreSQL (via pgAdmin)
- **ORM**: SQLAlchemy

## Prerequisites

- Python 3.9+
- PostgreSQL 14+
- pgAdmin (recommended for database management)

## Installation

### 1. Clone/Download the Project

```bash
cd car_service_system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Create a PostgreSQL database:

```sql
CREATE DATABASE car_service_db;
```

Copy `.env.example` to `.env` and update the database credentials:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=car_service_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### 5. Initialize Database

Run the initialization script to create tables and seed data:

```bash
python -m database.init_db
```

### 6. Run the Application

```bash
streamlit run app.py
```

## Pre-Made User Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@carservice.com | Admin@123 |
| Manager | manager@carservice.com | Manager@123 |
| Technician | tech@carservice.com | Tech@123 |
| Cashier | cashier@carservice.com | Cashier@123 |

## Project Structure

```
car_service_system/
├── app.py                    # Main entry point
├── config.py                 # Configuration settings
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── database/
│   ├── connection.py         # Database connection
│   ├── models.py             # SQLAlchemy models
│   └── init_db.py            # Database initialization
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Customers.py
│   ├── 3_Vehicles.py
│   ├── 4_Service_Orders.py
│   ├── 5_Inventory.py
│   ├── 6_POS.py
│   ├── 7_Invoices.py
│   └── 8_Reports.py
├── services/
│   ├── auth_service.py
│   ├── customer_service.py
│   ├── vehicle_service.py
│   ├── service_order_service.py
│   ├── inventory_service.py
│   ├── pos_service.py
│   └── invoice_service.py
├── utils/
│   ├── helpers.py
│   └── validators.py
├── static/
│   └── styles.css
└── sql/
    └── schema.sql
```

## Branding

The application uses the following brand colors:

- **Primary Accent (Lime Green)**: #D2FF32
- **Deep Charcoal/Black**: #111111
- **Pure White**: #FFFFFF
- **Text Secondary**: #555555
- **Light Grey Background**: #F8F9FA

**Typography**:
- Headings: Montserrat (Bold)
- Body: Poppins (Regular/Semi-bold)

## License

This project is for educational and internal use purposes.

## Support

For issues or questions, please contact the development team.
