#!/usr/bin/env python3
"""
Script to create an admin user for MealBridge
"""

from __init__ import create_app, db
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin_user():
    """Create an admin user in the database"""
    app = create_app()
    
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print("✅ Admin user already exists!")
            print(f"Username: {admin_user.username}")
            print(f"Email: {admin_user.email}")
            print(f"Role: {admin_user.role}")
            return
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@mealbridge.com',
            password_hash=generate_password_hash('admin123'),
            full_name='System Administrator',
            role='admin',
            phone='+1-555-0123',
            address='123 Admin Street, Admin City',
            is_verified=True,
            created_at=datetime.utcnow()
        )
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            
            print("🎉 Admin user created successfully!")
            print("=" * 50)
            print("Admin Credentials:")
            print("Username: admin")
            print("Password: admin123")
            print("Email: admin@mealbridge.com")
            print("Role: admin")
            print("=" * 50)
            print("⚠️  IMPORTANT: Change the default password after first login!")
            print("You can access the admin dashboard at: http://localhost:5000/admin/dashboard")
            
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            db.session.rollback()

if __name__ == "__main__":
    print("Creating Admin User for MealBridge...")
    print("=" * 50)
    create_admin_user()
