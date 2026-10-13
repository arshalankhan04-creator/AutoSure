"""
Clean Database Initialization - Easy Ride Auto Service
Complete rewrite with Indian pricing, proper Decimal usage, and clean seed data
"""

import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal
from passlib.context import CryptContext

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine, SessionLocal, Base
from database.models import (
    User, Customer, Vehicle, Technician, ServiceType, Part,
    ServiceOrder, ServiceItem, OrderPart, Invoice, Payment
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_tables():
    """Create all database tables"""
    print("🔧 Creating database tables...")
    Base.metadata.drop_all(bind=engine)  # Clean slate
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!\n")


def seed_users(db):
    """Create user accounts"""
    print("👥 Seeding users...")
    
    users = [
        {"username": "admin", "email": "admin@carservice.com", "password": "Admin@123",
         "full_name": "Rajesh Kumar", "role": "admin"},
        {"username": "manager", "email": "manager@carservice.com", "password": "Manager@123",
         "full_name": "Priya Sharma", "role": "manager"},
        {"username": "cashier", "email": "cashier@carservice.com", "password": "Cashier@123",
         "full_name": "Amit Patel", "role": "cashier"},
        {"username": "tech1", "email": "tech1@carservice.com", "password": "Tech@123",
         "full_name": "Vikram Singh", "role": "technician"},
        {"username": "tech2", "email": "tech2@carservice.com", "password": "Tech@123",
         "full_name": "Deepak Mehta", "role": "technician"},
        {"username": "tech3", "email": "tech3@carservice.com", "password": "Tech@123",
         "full_name": "Suresh Rao", "role": "technician"},
        {"username": "tech4", "email": "tech4@carservice.com", "password": "Tech@123",
         "full_name": "Anil Desai", "role": "technician"},
        {"username": "tech5", "email": "tech5@carservice.com", "password": "Tech@123",
         "full_name": "Kiran Joshi", "role": "technician"},
    ]
    
    for u in users:
        user = User(
            username=u["username"],
            email=u["email"],
            password_hash=hash_password(u["password"]),
            full_name=u["full_name"],
            role=u["role"],
            is_active=True
        )
        db.add(user)
        print(f"  ✓ {u['email']} ({u['role']})")
    
    db.commit()
    print("✅ Users created!\n")


def seed_technicians(db):
    """Create technician profiles"""
    print("🔧 Seeding technicians...")
    
    techs = [
        {"name": "Vikram Singh", "employee_id": "TECH-001", "specialty": "Engine & Transmission",
         "hourly_rate": Decimal("600.00"), "phone": "+91 98765 43201"},
        {"name": "Deepak Mehta", "employee_id": "TECH-002", "specialty": "Electrical & Electronics",
         "hourly_rate": Decimal("550.00"), "phone": "+91 98765 43202"},
        {"name": "Suresh Rao", "employee_id": "TECH-003", "specialty": "Brakes & Suspension",
         "hourly_rate": Decimal("500.00"), "phone": "+91 98765 43203"},
        {"name": "Anil Desai", "employee_id": "TECH-004", "specialty": "AC & Cooling Systems",
         "hourly_rate": Decimal("520.00"), "phone": "+91 98765 43204"},
        {"name": "Kiran Joshi", "employee_id": "TECH-005", "specialty": "General Service",
         "hourly_rate": Decimal("480.00"), "phone": "+91 98765 43205"},
    ]
    
    for t in techs:
        tech = Technician(**t)
        db.add(tech)
        print(f"  ✓ {t['name']} - {t['specialty']}")
    
    db.commit()
    
    # Link to user accounts
    tech_users = db.query(User).filter(User.role == 'technician').all()
    technicians = db.query(Technician).all()
    
    for i, user in enumerate(tech_users):
        if i < len(technicians):
            user.technician_id = technicians[i].id
    
    db.commit()
    print("✅ Technicians created and linked!\n")


def seed_service_types(db):
    """Create comprehensive service catalog with Indian pricing"""
    print("📋 Seeding service catalog...")
    
    services = [
        # Basic Maintenance (₹200-800)
        {"name": "Basic Car Wash", "description": "Exterior wash and dry", "category": "Cleaning",
         "standard_hours": Decimal("0.5"), "base_price": Decimal("200.00")},
        {"name": "Interior Cleaning", "description": "Vacuum and interior wipe", "category": "Cleaning",
         "standard_hours": Decimal("0.75"), "base_price": Decimal("350.00")},
        {"name": "Full Detailing", "description": "Complete interior and exterior detailing", "category": "Cleaning",
         "standard_hours": Decimal("3.0"), "base_price": Decimal("2500.00")},
        
        # Oil & Fluids (₹500-1500)
        {"name": "Engine Oil Change - Mineral", "description": "Standard mineral oil change with filter",
         "category": "Maintenance", "standard_hours": Decimal("0.5"), "base_price": Decimal("500.00")},
        {"name": "Engine Oil Change - Synthetic", "description": "Premium synthetic oil change with filter",
         "category": "Maintenance", "standard_hours": Decimal("0.5"), "base_price": Decimal("1200.00")},
        {"name": "Coolant Flush", "description": "Radiator flush and coolant replacement", "category": "Cooling",
         "standard_hours": Decimal("1.0"), "base_price": Decimal("800.00")},
        {"name": "Transmission Fluid Change", "description": "Transmission fluid and filter change",
         "category": "Transmission", "standard_hours": Decimal("1.5"), "base_price": Decimal("1500.00")},
        {"name": "Brake Fluid Flush", "description": "Complete brake fluid system flush", "category": "Brakes",
         "standard_hours": Decimal("1.0"), "base_price": Decimal("600.00")},
        
        # Filters (₹150-500)
        {"name": "Air Filter Replacement", "description": "Engine air filter replacement", "category": "Maintenance",
         "standard_hours": Decimal("0.25"), "base_price": Decimal("150.00")},
        {"name": "Cabin Air Filter Replacement", "description": "Replace cabin air filter", "category": "Maintenance",
         "standard_hours": Decimal("0.25"), "base_price": Decimal("200.00")},
        {"name": "Fuel Filter Replacement", "description": "Replace fuel filter", "category": "Engine",
         "standard_hours": Decimal("0.75"), "base_price": Decimal("450.00")},
        
        # Brakes (₹800-3000)
        {"name": "Brake Pad Replacement - Front", "description": "Front brake pad replacement (labor only)",
         "category": "Brakes", "standard_hours": Decimal("1.5"), "base_price": Decimal("1200.00")},
        {"name": "Brake Pad Replacement - Rear", "description": "Rear brake pad replacement (labor only)",
         "category": "Brakes", "standard_hours": Decimal("1.5"), "base_price": Decimal("1000.00")},
        {"name": "Brake Rotor Replacement", "description": "Brake rotor replacement (labor only)",
         "category": "Brakes", "standard_hours": Decimal("2.0"), "base_price": Decimal("1500.00")},
        {"name": "Brake Inspection", "description": "Comprehensive brake system inspection", "category": "Brakes",
         "standard_hours": Decimal("0.5"), "base_price": Decimal("300.00")},
        
        # Tires & Wheels (₹300-1200)
        {"name": "Tire Rotation", "description": "Four tire rotation and pressure check", "category": "Maintenance",
         "standard_hours": Decimal("0.5"), "base_price": Decimal("300.00")},
        {"name": "Wheel Alignment", "description": "Four-wheel alignment adjustment", "category": "Suspension",
         "standard_hours": Decimal("1.0"), "base_price": Decimal("1000.00")},
        {"name": "Wheel Balancing", "description": "Balance all four wheels", "category": "Maintenance",
         "standard_hours": Decimal("0.75"), "base_price": Decimal("600.00")},
        {"name": "Puncture Repair", "description": "Tire puncture repair", "category": "Maintenance",
         "standard_hours": Decimal("0.5"), "base_price": Decimal("200.00")},
        
        # Engine Services (₹800-2500)
        {"name": "Engine Diagnostic", "description": "Complete computer diagnostic scan", "category": "Diagnostics",
         "standard_hours": Decimal("1.0"), "base_price": Decimal("800.00")},
        {"name": "Spark Plug Replacement", "description": "Replace all spark plugs", "category": "Engine",
         "standard_hours": Decimal("1.5"), "base_price": Decimal("1200.00")},
        {"name": "Timing Belt Replacement", "description": "Replace timing belt", "category": "Engine",
         "standard_hours": Decimal("3.0"), "base_price": Decimal("2500.00")},
        
        # Electrical (₹300-2000)
        {"name": "Battery Replacement", "description": "Battery testing and replacement (labor only)",
         "category": "Electrical", "standard_hours": Decimal("0.5"), "base_price": Decimal("300.00")},
        {"name": "Battery Testing", "description": "Battery and charging system test", "category": "Electrical",
         "standard_hours": Decimal("0.25"), "base_price": Decimal("150.00")},
        {"name": "Alternator Replacement", "description": "Replace alternator (labor only)", "category": "Electrical",
         "standard_hours": Decimal("2.0"), "base_price": Decimal("1800.00")},
        {"name": "Starter Motor Replacement", "description": "Replace starter motor (labor only)",
         "category": "Electrical", "standard_hours": Decimal("1.5"), "base_price": Decimal("1500.00")},
        {"name": "Headlight Bulb Replacement", "description": "Replace headlight bulbs", "category": "Electrical",
         "standard_hours": Decimal("0.5"), "base_price": Decimal("250.00")},
        {"name": "Horn Replacement", "description": "Replace horn", "category": "Electrical",
         "standard_hours": Decimal("0.5"), "base_price": Decimal("200.00")},
        
        # AC Services (₹800-3500)
        {"name": "AC Gas Recharge", "description": "Air conditioning refrigerant recharge", "category": "Climate Control",
         "standard_hours": Decimal("1.0"), "base_price": Decimal("1200.00")},
        {"name": "AC Compressor Replacement", "description": "Replace AC compressor (labor only)",
         "category": "Climate Control", "standard_hours": Decimal("3.0"), "base_price": Decimal("2800.00")},
        {"name": "AC System Inspection", "description": "Complete AC system diagnostic", "category": "Climate Control",
         "standard_hours": Decimal("0.75"), "base_price": Decimal("500.00")},
        
        # Exterior (₹150-2000)
        {"name": "Wiper Blade Replacement", "description": "Replace windshield wiper blades", "category": "Exterior",
         "standard_hours": Decimal("0.25"), "base_price": Decimal("150.00")},
        {"name": "Side Mirror Replacement", "description": "Replace side mirror (labor only)", "category": "Exterior",
         "standard_hours": Decimal("0.75"), "base_price": Decimal("600.00")},
        {"name": "Headlight Restoration", "description": "Restore foggy headlights", "category": "Exterior",
         "standard_hours": Decimal("1.0"), "base_price": Decimal("800.00")},
        
        # Inspection (₹500-1500)
        {"name": "Pre-Purchase Inspection", "description": "Comprehensive vehicle inspection",
         "category": "Inspection", "standard_hours": Decimal("2.0"), "base_price": Decimal("1200.00")},
        {"name": "Safety Inspection", "description": "Complete safety system check", "category": "Inspection",
         "standard_hours": Decimal("1.0"), "base_price": Decimal("600.00")},
        {"name": "Emission Test", "description": "Emission system testing", "category": "Inspection",
         "standard_hours": Decimal("0.5"), "base_price": Decimal("400.00")},
    ]
    
    for s in services:
        service = ServiceType(**s)
        db.add(service)
    
    db.commit()
    print(f"✅ Created {len(services)} service types!\n")


def seed_parts(db):
    """Create parts inventory with Indian pricing"""
    print("📦 Seeding parts inventory...")
    
    parts = [
        # Fluids (OIL-xxx)
        {"sku": "OIL-001", "name": "Engine Oil 5W-30 Synthetic (4L)", "category": "Fluids",
         "cost_price": Decimal("1200.00"), "selling_price": Decimal("1800.00"),
         "stock_quantity": 50, "reorder_level": 20, "location": "Shelf A-1"},
        {"sku": "OIL-002", "name": "Engine Oil 10W-40 Mineral (4L)", "category": "Fluids",
         "cost_price": Decimal("600.00"), "selling_price": Decimal("900.00"),
         "stock_quantity": 60, "reorder_level": 25, "location": "Shelf A-1"},
        {"sku": "OIL-003", "name": "Brake Fluid DOT 4 (500ml)", "category": "Fluids",
         "cost_price": Decimal("150.00"), "selling_price": Decimal("250.00"),
         "stock_quantity": 40, "reorder_level": 15, "location": "Shelf A-2"},
        {"sku": "OIL-004", "name": "Coolant/Antifreeze (1L)", "category": "Fluids",
         "cost_price": Decimal("200.00"), "selling_price": Decimal("350.00"),
         "stock_quantity": 35, "reorder_level": 15, "location": "Shelf A-2"},
        {"sku": "OIL-005", "name": "Transmission Fluid ATF (1L)", "category": "Fluids",
         "cost_price": Decimal("300.00"), "selling_price": Decimal("500.00"),
         "stock_quantity": 30, "reorder_level": 12, "location": "Shelf A-2"},
        
        # Filters (FLT-xxx)
        {"sku": "FLT-001", "name": "Oil Filter - Standard", "category": "Filters",
         "cost_price": Decimal("150.00"), "selling_price": Decimal("300.00"),
         "stock_quantity": 100, "reorder_level": 30, "location": "Shelf B-1"},
        {"sku": "FLT-002", "name": "Air Filter - Standard", "category": "Filters",
         "cost_price": Decimal("200.00"), "selling_price": Decimal("400.00"),
         "stock_quantity": 60, "reorder_level": 20, "location": "Shelf B-1"},
        {"sku": "FLT-003", "name": "Cabin Air Filter", "category": "Filters",
         "cost_price": Decimal("250.00"), "selling_price": Decimal("500.00"),
         "stock_quantity": 40, "reorder_level": 15, "location": "Shelf B-1"},
        {"sku": "FLT-004", "name": "Fuel Filter", "category": "Filters",
         "cost_price": Decimal("180.00"), "selling_price": Decimal("350.00"),
         "stock_quantity": 35, "reorder_level": 12, "location": "Shelf B-2"},
        
        # Brakes (BRK-xxx)
        {"sku": "BRK-001", "name": "Brake Pads - Front Ceramic", "category": "Brakes",
         "cost_price": Decimal("1200.00"), "selling_price": Decimal("2000.00"),
         "stock_quantity": 25, "reorder_level": 10, "location": "Shelf C-1"},
        {"sku": "BRK-002", "name": "Brake Pads - Rear Ceramic", "category": "Brakes",
         "cost_price": Decimal("1000.00"), "selling_price": Decimal("1700.00"),
         "stock_quantity": 25, "reorder_level": 10, "location": "Shelf C-1"},
        {"sku": "BRK-003", "name": "Brake Rotors - Front Pair", "category": "Brakes",
         "cost_price": Decimal("2000.00"), "selling_price": Decimal("3500.00"),
         "stock_quantity": 15, "reorder_level": 5, "location": "Shelf C-2"},
        {"sku": "BRK-004", "name": "Brake Rotors - Rear Pair", "category": "Brakes",
         "cost_price": Decimal("1800.00"), "selling_price": Decimal("3200.00"),
         "stock_quantity": 15, "reorder_level": 5, "location": "Shelf C-2"},
        
        # Electrical (ELC-xxx)
        {"sku": "ELC-001", "name": "Car Battery 12V 65Ah", "category": "Electrical",
         "cost_price": Decimal("3500.00"), "selling_price": Decimal("5500.00"),
         "stock_quantity": 12, "reorder_level": 5, "location": "Shelf D-1"},
        {"sku": "ELC-002", "name": "Alternator Belt", "category": "Electrical",
         "cost_price": Decimal("200.00"), "selling_price": Decimal("400.00"),
         "stock_quantity": 30, "reorder_level": 10, "location": "Shelf D-2"},
        {"sku": "ELC-003", "name": "Headlight Bulb H4", "category": "Electrical",
         "cost_price": Decimal("150.00"), "selling_price": Decimal("300.00"),
         "stock_quantity": 50, "reorder_level": 20, "location": "Shelf D-3"},
        {"sku": "ELC-004", "name": "Horn - Standard", "category": "Electrical",
         "cost_price": Decimal("200.00"), "selling_price": Decimal("400.00"),
         "stock_quantity": 25, "reorder_level": 10, "location": "Shelf D-3"},
        
        # Ignition (IGN-xxx)
        {"sku": "IGN-001", "name": "Spark Plugs (Set of 4)", "category": "Ignition",
         "cost_price": Decimal("600.00"), "selling_price": Decimal("1000.00"),
         "stock_quantity": 30, "reorder_level": 10, "location": "Shelf E-1"},
        {"sku": "IGN-002", "name": "Ignition Coil", "category": "Ignition",
         "cost_price": Decimal("800.00"), "selling_price": Decimal("1400.00"),
         "stock_quantity": 15, "reorder_level": 5, "location": "Shelf E-1"},
        
        # Exterior (EXT-xxx)
        {"sku": "EXT-001", "name": "Wiper Blades (Pair)", "category": "Exterior",
         "cost_price": Decimal("300.00"), "selling_price": Decimal("600.00"),
         "stock_quantity": 45, "reorder_level": 15, "location": "Shelf F-1"},
        {"sku": "EXT-002", "name": "Side Mirror - Left", "category": "Exterior",
         "cost_price": Decimal("800.00"), "selling_price": Decimal("1500.00"),
         "stock_quantity": 10, "reorder_level": 3, "location": "Shelf F-2"},
        {"sku": "EXT-003", "name": "Side Mirror - Right", "category": "Exterior",
         "cost_price": Decimal("800.00"), "selling_price": Decimal("1500.00"),
         "stock_quantity": 10, "reorder_level": 3, "location": "Shelf F-2"},
    ]
    
    for p in parts:
        part = Part(**p)
        db.add(part)
    
    db.commit()
    print(f"✅ Created {len(parts)} parts!\n")


def seed_customers(db):
    """Create sample customers with Indian names"""
    print("👥 Seeding customers...")
    
    customers = [
        {"name": "Arjun Patel", "phone": "+91 98765 11111", "email": "arjun.patel@email.com",
         "address": "123 MG Road, Ahmedabad, Gujarat 380001", "customer_type": "regular"},
        {"name": "Priya Desai", "phone": "+91 98765 22222", "email": "priya.desai@email.com",
         "address": "456 CG Road, Ahmedabad, Gujarat 380009", "customer_type": "vip"},
        {"name": "Rahul Shah", "phone": "+91 98765 33333", "email": "rahul.shah@email.com",
         "address": "789 SG Highway, Ahmedabad, Gujarat 380015", "customer_type": "regular"},
        {"name": "Neha Mehta", "phone": "+91 98765 44444", "email": "neha.mehta@email.com",
         "address": "321 Satellite Road, Ahmedabad, Gujarat 380015", "customer_type": "regular"},
        {"name": "Gujarat Auto Parts Ltd", "phone": "+91 98765 55555", "email": "orders@gujaratauto.com",
         "address": "555 GIDC Estate, Vatva, Ahmedabad, Gujarat 382445", "customer_type": "wholesale"},
    ]
    
    for c in customers:
        customer = Customer(**c)
        db.add(customer)
        print(f"  ✓ {c['name']}")
    
    db.commit()
    print("✅ Customers created!\n")


def seed_vehicles(db):
    """Create sample vehicles with Gujarat license plates"""
    print("🚗 Seeding vehicles...")
    
    customers = db.query(Customer).all()
    
    vehicles = [
        {"make": "Maruti Suzuki", "model": "Swift", "year": 2022, "license_plate": "GJ01AB1234",
         "vin": "MA3EYD81S00123456", "color": "Red", "current_mileage": 15000},
        {"make": "Hyundai", "model": "Creta", "year": 2021, "license_plate": "GJ01CD5678",
         "vin": "MALH11CKXM1234567", "color": "White", "current_mileage": 28000},
        {"make": "Tata", "model": "Nexon", "year": 2023, "license_plate": "GJ01EF9012",
         "vin": "MAT622HPXN1234567", "color": "Blue", "current_mileage": 8000},
        {"make": "Honda", "model": "City", "year": 2020, "license_plate": "GJ01GH3456",
         "vin": "MRHFB18120123456", "color": "Silver", "current_mileage": 45000},
        {"make": "Mahindra", "model": "Scorpio", "year": 2019, "license_plate": "GJ01JK7890",
         "vin": "MA1TA2GKXJ1234567", "color": "Black", "current_mileage": 62000},
    ]
    
    for i, v in enumerate(vehicles):
        if i < len(customers):
            vehicle = Vehicle(customer_id=customers[i].id, **v)
            db.add(vehicle)
            print(f"  ✓ {v['make']} {v['model']} - {v['license_plate']}")
    
    db.commit()
    print("✅ Vehicles created!\n")


def main():
    """Main initialization"""
    print("\n" + "="*60)
    print("🔧 EASY RIDE AUTO SERVICE - Database Initialization")
    print("="*60 + "\n")
    
    create_tables()
    
    db = SessionLocal()
    try:
        seed_users(db)
        seed_technicians(db)
        seed_service_types(db)
        seed_parts(db)
        seed_customers(db)
        seed_vehicles(db)
        
        print("="*60)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("="*60)
        
        print("\n📋 LOGIN CREDENTIALS:")
        print("-"*60)
        print("  Admin:       admin / Admin@123")
        print("  Manager:     manager / Manager@123")
        print("  Cashier:     cashier / Cashier@123")
        print("  Technician1: tech1 / Tech@123")
        print("  Technician2: tech2 / Tech@123")
        print("  Technician3: tech3 / Tech@123")
        print("  Technician4: tech4 / Tech@123")
        print("  Technician5: tech5 / Tech@123")
        print("-"*60)
        print("\n🚀 Ready to launch: streamlit run app.py\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
