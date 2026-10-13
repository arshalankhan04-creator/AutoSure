"""
Database Initialization Script
Creates tables and seeds initial data including pre-made user accounts
"""

import sys
import os
from datetime import datetime, date, timedelta
from passlib.context import CryptContext

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from database.connection import engine, SessionLocal, Base
from database.models import (
    User, Customer, Vehicle, Technician, ServiceType, Part,
    ServiceOrder, ServiceItem, OrderPart, Invoice, Payment
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully!")


def seed_users(db):
    """Create pre-made user accounts including technicians"""
    print("\nSeeding users...")
    
    users_data = [
        {
            "username": "admin",
            "email": "admin@carservice.com",
            "password": "Admin@123",
            "full_name": "John Admin",
            "role": "admin"
        },
        {
            "username": "manager",
            "email": "manager@carservice.com",
            "password": "Manager@123",
            "full_name": "Sarah Manager",
            "role": "manager"
        },
        {
            "username": "cashier",
            "email": "cashier@carservice.com",
            "password": "Cashier@123",
            "full_name": "Lisa Cashier",
            "role": "cashier"
        },
        {
            "username": "tech1",
            "email": "tech1@carservice.com",
            "password": "Tech@123",
            "full_name": "David Martinez",
            "role": "technician"
        },
        {
            "username": "tech2",
            "email": "tech2@carservice.com",
            "password": "Tech@123",
            "full_name": "Sarah Thompson",
            "role": "technician"
        },
        {
            "username": "tech3",
            "email": "tech3@carservice.com",
            "password": "Tech@123",
            "full_name": "Michael Brown",
            "role": "technician"
        },
        {
            "username": "tech4",
            "email": "tech4@carservice.com",
            "password": "Tech@123",
            "full_name": "Lisa Anderson",
            "role": "technician"
        },
        {
            "username": "tech5",
            "email": "tech5@carservice.com",
            "password": "Tech@123",
            "full_name": "James Wilson",
            "role": "technician"
        }
    ]
    
    for user_data in users_data:
        # Check if user exists
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"  - User {user_data['email']} already exists, skipping...")
            continue
        
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=hash_password(user_data["password"]),
            full_name=user_data["full_name"],
            role=user_data["role"],
            is_active=True
        )
        db.add(user)
        print(f"  ✓ Created user: {user_data['email']} ({user_data['role']})")
    
    db.commit()
    print("✓ Users seeded successfully!")


def seed_customers(db):
    """Create sample customers"""
    print("\nSeeding customers...")
    
    customers_data = [
        {"name": "James Wilson", "phone": "555-0101", "email": "james.wilson@email.com", 
         "address": "123 Main Street, Springfield, IL 62701", "customer_type": "regular"},
        {"name": "Maria Garcia", "phone": "555-0102", "email": "maria.garcia@email.com",
         "address": "456 Oak Avenue, Chicago, IL 60601", "customer_type": "vip"},
        {"name": "Robert Chen", "phone": "555-0103", "email": "robert.chen@email.com",
         "address": "789 Pine Road, Naperville, IL 60540", "customer_type": "wholesale"},
        {"name": "Emily Johnson", "phone": "555-0104", "email": "emily.j@email.com",
         "address": "321 Elm Street, Evanston, IL 60201", "customer_type": "regular"},
        {"name": "Auto Parts Plus LLC", "phone": "555-0105", "email": "orders@autopartsplus.com",
         "address": "555 Commerce Drive, Aurora, IL 60502", "customer_type": "wholesale"},
    ]
    
    for data in customers_data:
        existing = db.query(Customer).filter(Customer.email == data["email"]).first()
        if existing:
            continue
        
        customer = Customer(**data)
        db.add(customer)
    
    db.commit()
    print(f"✓ Created {len(customers_data)} sample customers!")


def seed_vehicles(db):
    """Create sample vehicles"""
    print("\nSeeding vehicles...")
    
    customers = db.query(Customer).all()
    if not customers:
        print("  ! No customers found, skipping vehicles...")
        return
    
    vehicles_data = [
        {"make": "Toyota", "model": "Camry", "year": 2020, "license_plate": "ABC-1234",
         "vin": "1HGBH41JXMN109186", "color": "Silver", "current_mileage": 45000},
        {"make": "Honda", "model": "CR-V", "year": 2019, "license_plate": "XYZ-5678",
         "vin": "2HGFC2F59KH534627", "color": "Blue", "current_mileage": 62000},
        {"make": "Ford", "model": "F-150", "year": 2021, "license_plate": "TRK-9012",
         "vin": "1FTEW1E53MFA12345", "color": "Black", "current_mileage": 28000},
        {"make": "BMW", "model": "3 Series", "year": 2022, "license_plate": "BMV-3456",
         "vin": "WBA8E9C55KAB12345", "color": "White", "current_mileage": 15000},
        {"make": "Chevrolet", "model": "Silverado", "year": 2018, "license_plate": "CHV-7890",
         "vin": "3GCUYDED4JG123456", "color": "Red", "current_mileage": 85000},
    ]
    
    for i, data in enumerate(vehicles_data):
        if i >= len(customers):
            break
        
        existing = db.query(Vehicle).filter(Vehicle.license_plate == data["license_plate"]).first()
        if existing:
            continue
        
        vehicle = Vehicle(customer_id=customers[i].id, **data)
        db.add(vehicle)
    
    db.commit()
    print(f"✓ Created {min(len(vehicles_data), len(customers))} sample vehicles!")


def seed_technicians(db):
    """Create sample technicians matching user accounts"""
    print("\nSeeding technicians...")
    
    technicians_data = [
        {"name": "David Martinez", "employee_id": "TECH-001", "specialty": "Engine Repair",
         "hourly_rate": 75.00, "phone": "555-0201"},
        {"name": "Sarah Thompson", "employee_id": "TECH-002", "specialty": "Electrical Systems",
         "hourly_rate": 80.00, "phone": "555-0202"},
        {"name": "Michael Brown", "employee_id": "TECH-003", "specialty": "Brakes & Suspension",
         "hourly_rate": 70.00, "phone": "555-0203"},
        {"name": "Lisa Anderson", "employee_id": "TECH-004", "specialty": "General Service",
         "hourly_rate": 65.00, "phone": "555-0204"},
        {"name": "James Wilson", "employee_id": "TECH-005", "specialty": "Transmission & Drivetrain",
         "hourly_rate": 85.00, "phone": "555-0205"},
    ]
    
    for data in technicians_data:
        existing = db.query(Technician).filter(Technician.employee_id == data["employee_id"]).first()
        if existing:
            continue
        
        technician = Technician(**data)
        db.add(technician)
    
    db.commit()
    
    # Link technicians to user accounts
    print("  Linking technicians to user accounts...")
    tech_users = db.query(User).filter(User.role == 'technician').all()
    technicians = db.query(Technician).all()
    
    for i, user in enumerate(tech_users):
        if i < len(technicians):
            user.technician_id = technicians[i].id
    
    db.commit()
    print(f"✓ Created {len(technicians_data)} technicians and linked to user accounts!")


def seed_service_types(db):
    """Create comprehensive service types catalog with fixed prices"""
    print("\nSeeding service types...")
    
    services_data = [
        # Basic Maintenance Services
        {"name": "Oil Change - Conventional", "description": "Standard oil change with conventional oil and filter",
         "category": "Maintenance", "standard_hours": 0.5, "base_price": 35.00},
        {"name": "Oil Change - Synthetic", "description": "Premium synthetic oil change with filter replacement",
         "category": "Maintenance", "standard_hours": 0.5, "base_price": 65.00},
        {"name": "Tire Rotation", "description": "Four tire rotation and pressure check",
         "category": "Maintenance", "standard_hours": 0.5, "base_price": 25.00},
        {"name": "Wheel Alignment", "description": "Four-wheel alignment adjustment",
         "category": "Suspension", "standard_hours": 1.0, "base_price": 85.00},
        {"name": "Wheel Balancing", "description": "Balance all four wheels",
         "category": "Maintenance", "standard_hours": 0.75, "base_price": 45.00},
        
        # Brake Services
        {"name": "Brake Pad Replacement - Front", "description": "Front brake pad replacement (labor only)",
         "category": "Brakes", "standard_hours": 1.5, "base_price": 120.00},
        {"name": "Brake Pad Replacement - Rear", "description": "Rear brake pad replacement (labor only)",
         "category": "Brakes", "standard_hours": 1.5, "base_price": 110.00},
        {"name": "Brake Rotor Replacement", "description": "Brake rotor replacement (labor only)",
         "category": "Brakes", "standard_hours": 2.0, "base_price": 150.00},
        {"name": "Brake Fluid Flush", "description": "Complete brake fluid system flush",
         "category": "Brakes", "standard_hours": 1.0, "base_price": 80.00},
        {"name": "Brake Inspection", "description": "Comprehensive brake system inspection",
         "category": "Brakes", "standard_hours": 0.5, "base_price": 30.00},
        
        # Engine Services
        {"name": "Engine Diagnostic", "description": "Complete computer diagnostic scan",
         "category": "Diagnostics", "standard_hours": 1.0, "base_price": 95.00},
        {"name": "Spark Plug Replacement", "description": "Replace all spark plugs",
         "category": "Engine", "standard_hours": 1.5, "base_price": 125.00},
        {"name": "Air Filter Replacement", "description": "Engine air filter replacement",
         "category": "Maintenance", "standard_hours": 0.25, "base_price": 20.00},
        {"name": "Cabin Air Filter Replacement", "description": "Replace cabin air filter",
         "category": "Maintenance", "standard_hours": 0.25, "base_price": 25.00},
        {"name": "Fuel Filter Replacement", "description": "Replace fuel filter",
         "category": "Engine", "standard_hours": 0.75, "base_price": 65.00},
        {"name": "Coolant Flush", "description": "Radiator flush and coolant replacement",
         "category": "Cooling", "standard_hours": 1.0, "base_price": 95.00},
        {"name": "Transmission Fluid Change", "description": "Transmission fluid change and filter",
         "category": "Transmission", "standard_hours": 1.5, "base_price": 175.00},
        {"name": "Transmission Flush", "description": "Complete transmission system flush",
         "category": "Transmission", "standard_hours": 2.0, "base_price": 225.00},
        
        # Electrical Services
        {"name": "Battery Replacement", "description": "Battery testing and replacement (labor only)",
         "category": "Electrical", "standard_hours": 0.5, "base_price": 35.00},
        {"name": "Battery Testing", "description": "Battery and charging system test",
         "category": "Electrical", "standard_hours": 0.25, "base_price": 15.00},
        {"name": "Alternator Replacement", "description": "Replace alternator (labor only)",
         "category": "Electrical", "standard_hours": 2.0, "base_price": 180.00},
        {"name": "Starter Motor Replacement", "description": "Replace starter motor (labor only)",
         "category": "Electrical", "standard_hours": 1.5, "base_price": 150.00},
        {"name": "Headlight Bulb Replacement", "description": "Replace headlight bulbs",
         "category": "Electrical", "standard_hours": 0.5, "base_price": 30.00},
        {"name": "Wiring Repair", "description": "Electrical wiring diagnosis and repair",
         "category": "Electrical", "standard_hours": 2.0, "base_price": 160.00},
        
        # Climate Control
        {"name": "AC Recharge", "description": "Air conditioning refrigerant recharge",
         "category": "Climate Control", "standard_hours": 1.0, "base_price": 125.00},
        {"name": "AC Compressor Replacement", "description": "Replace AC compressor (labor only)",
         "category": "Climate Control", "standard_hours": 3.0, "base_price": 280.00},
        {"name": "AC System Inspection", "description": "Complete AC system diagnostic",
         "category": "Climate Control", "standard_hours": 0.75, "base_price": 65.00},
        {"name": "Heater Core Replacement", "description": "Replace heater core (labor only)",
         "category": "Climate Control", "standard_hours": 4.0, "base_price": 350.00},
        
        # Exterior Services
        {"name": "Wiper Blade Replacement", "description": "Replace windshield wiper blades",
         "category": "Exterior", "standard_hours": 0.25, "base_price": 15.00},
        {"name": "Windshield Replacement", "description": "Replace windshield (labor only)",
         "category": "Exterior", "standard_hours": 2.0, "base_price": 200.00},
        {"name": "Side Mirror Replacement", "description": "Replace side mirror (labor only)",
         "category": "Exterior", "standard_hours": 0.75, "base_price": 65.00},
        
        # Cleaning & Detailing
        {"name": "Basic Car Wash", "description": "Exterior wash and dry",
         "category": "Cleaning", "standard_hours": 0.5, "base_price": 20.00},
        {"name": "Full Detail", "description": "Complete interior and exterior detailing",
         "category": "Cleaning", "standard_hours": 3.0, "base_price": 150.00},
        {"name": "Interior Vacuum & Clean", "description": "Interior vacuuming and surface cleaning",
         "category": "Cleaning", "standard_hours": 0.75, "base_price": 35.00},
        
        # Inspection Services
        {"name": "Pre-Purchase Inspection", "description": "Comprehensive vehicle inspection",
         "category": "Inspection", "standard_hours": 2.0, "base_price": 125.00},
        {"name": "Safety Inspection", "description": "Complete safety system check",
         "category": "Inspection", "standard_hours": 1.0, "base_price": 75.00},
        {"name": "Emission Test", "description": "Emission system testing",
         "category": "Inspection", "standard_hours": 0.5, "base_price": 45.00},
    ]
    
    for data in services_data:
        existing = db.query(ServiceType).filter(ServiceType.name == data["name"]).first()
        if existing:
            continue
        
        service = ServiceType(**data)
        db.add(service)
    
    db.commit()
    print(f"✓ Created {len(services_data)} service types!")


def seed_parts(db):
    """Create sample parts/inventory"""
    print("\nSeeding parts inventory...")
    
    parts_data = [
        {"sku": "OIL-001", "name": "Synthetic Motor Oil 5W-30 (5qt)", "category": "Fluids",
         "cost_price": 22.00, "selling_price": 35.99, "stock_quantity": 50, "reorder_level": 20, "location": "Aisle A-1"},
        {"sku": "FLT-001", "name": "Oil Filter - Standard", "category": "Filters",
         "cost_price": 4.50, "selling_price": 8.99, "stock_quantity": 100, "reorder_level": 30, "location": "Aisle A-2"},
        {"sku": "BRK-001", "name": "Brake Pads - Front Ceramic", "category": "Brakes",
         "cost_price": 35.00, "selling_price": 59.99, "stock_quantity": 25, "reorder_level": 10, "location": "Aisle B-1"},
        {"sku": "BRK-002", "name": "Brake Pads - Rear Ceramic", "category": "Brakes",
         "cost_price": 32.00, "selling_price": 54.99, "stock_quantity": 25, "reorder_level": 10, "location": "Aisle B-1"},
        {"sku": "BRK-003", "name": "Brake Rotors - Front Pair", "category": "Brakes",
         "cost_price": 55.00, "selling_price": 89.99, "stock_quantity": 15, "reorder_level": 5, "location": "Aisle B-2"},
        {"sku": "AIR-001", "name": "Air Filter - Standard", "category": "Filters",
         "cost_price": 8.00, "selling_price": 15.99, "stock_quantity": 60, "reorder_level": 20, "location": "Aisle A-3"},
        {"sku": "AIR-002", "name": "Cabin Air Filter", "category": "Filters",
         "cost_price": 10.00, "selling_price": 19.99, "stock_quantity": 40, "reorder_level": 15, "location": "Aisle A-3"},
        {"sku": "BAT-001", "name": "Car Battery 12V 60Ah", "category": "Electrical",
         "cost_price": 75.00, "selling_price": 129.99, "stock_quantity": 12, "reorder_level": 5, "location": "Aisle C-1"},
        {"sku": "SPK-001", "name": "Spark Plugs (Set of 4)", "category": "Ignition",
         "cost_price": 18.00, "selling_price": 32.99, "stock_quantity": 30, "reorder_level": 10, "location": "Aisle C-2"},
        {"sku": "WPR-001", "name": "Wiper Blades (Pair)", "category": "Exterior",
         "cost_price": 12.00, "selling_price": 24.99, "stock_quantity": 45, "reorder_level": 15, "location": "Aisle D-1"},
        {"sku": "ANT-001", "name": "Engine Coolant (1 Gallon)", "category": "Fluids",
         "cost_price": 8.00, "selling_price": 14.99, "stock_quantity": 35, "reorder_level": 15, "location": "Aisle A-1"},
        {"sku": "TRN-001", "name": "Transmission Fluid (1 Quart)", "category": "Fluids",
         "cost_price": 6.50, "selling_price": 12.99, "stock_quantity": 40, "reorder_level": 15, "location": "Aisle A-1"},
    ]
    
    for data in parts_data:
        existing = db.query(Part).filter(Part.sku == data["sku"]).first()
        if existing:
            continue
        
        part = Part(**data)
        db.add(part)
    
    db.commit()
    print(f"✓ Created {len(parts_data)} sample parts!")


def seed_sample_orders(db):
    """Create sample service orders for demonstration"""
    print("\nSeeding sample service orders...")
    
    customers = db.query(Customer).limit(3).all()
    vehicles = db.query(Vehicle).limit(3).all()
    technicians = db.query(Technician).limit(3).all()
    service_types = db.query(ServiceType).limit(3).all()
    parts = db.query(Part).limit(3).all()
    
    if not all([customers, vehicles, technicians, service_types]):
        print("  ! Missing prerequisite data, skipping sample orders...")
        return
    
    # Create a sample service order
    order = ServiceOrder(
        order_number=f"WO-{datetime.now().strftime('%Y%m%d')}-0001",
        customer_id=customers[0].id,
        vehicle_id=vehicles[0].id,
        technician_id=technicians[0].id,
        status="completed",
        complaint="Engine making unusual noise",
        diagnosis="Worn serpentine belt, needs replacement",
        notes="Customer requested quick turnaround",
        created_at=datetime.now() - timedelta(days=7),
        completed_at=datetime.now() - timedelta(days=5)
    )
    db.add(order)
    db.flush()
    
    # Add service items
    service_item = ServiceItem(
        service_order_id=order.id,
        service_type_id=service_types[0].id,
        description="Oil Change Service",
        labor_hours=0.5,
        labor_rate=75.00,
        labor_cost=37.50,
        status="completed"
    )
    db.add(service_item)
    
    # Add parts to order
    if parts:
        order_part = OrderPart(
            service_order_id=order.id,
            part_id=parts[0].id,
            quantity=1,
            unit_price=parts[0].selling_price,
            total_price=parts[0].selling_price
        )
        db.add(order_part)
    
    order.calculate_totals()
    db.commit()
    print(f"✓ Created sample service orders!")


def generate_order_number(db):
    """Generate a unique order number"""
    today = datetime.now().strftime('%Y%m%d')
    prefix = f"WO-{today}-"
    
    # Get the count of orders created today
    count = db.query(ServiceOrder).filter(
        ServiceOrder.order_number.like(f"{prefix}%")
    ).count() + 1
    
    return f"{prefix}{count:04d}"


def generate_invoice_number(db):
    """Generate a unique invoice number"""
    today = datetime.now().strftime('%Y%m%d')
    prefix = f"INV-{today}-"
    
    count = db.query(Invoice).filter(
        Invoice.invoice_number.like(f"{prefix}%")
    ).count() + 1
    
    return f"{prefix}{count:03d}"


def main():
    """Main initialization function"""
    print("=" * 50)
    print("AutoSure")
    print("Database Initialization")
    print("=" * 50)
    
    # Create tables
    create_tables()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Seed all data
        seed_users(db)
        seed_customers(db)
        seed_vehicles(db)
        seed_technicians(db)
        seed_service_types(db)
        seed_parts(db)
        seed_sample_orders(db)
        
        print("\n" + "=" * 50)
        print("✓ Database initialization complete!")
        print("=" * 50)
        
        print("\n📋 Pre-made User Accounts:")
        print("-" * 40)
        print("  Admin:       admin@carservice.com / Admin@123")
        print("  Manager:     manager@carservice.com / Manager@123")
        print("  Cashier:     cashier@carservice.com / Cashier@123")
        print("  Technician1: tech1@carservice.com / Tech@123")
        print("  Technician2: tech2@carservice.com / Tech@123")
        print("  Technician3: tech3@carservice.com / Tech@123")
        print("  Technician4: tech4@carservice.com / Tech@123")
        print("  Technician5: tech5@carservice.com / Tech@123")
        print("-" * 40)
        
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
