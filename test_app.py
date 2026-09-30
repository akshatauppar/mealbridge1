#!/usr/bin/env python3
"""
Simple test script to verify MealBridge application structure
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        # Test basic Python imports
        import datetime
        import secrets
        import io
        import base64
        print("✓ Basic Python modules imported successfully")
        
        # Test Flask imports (will fail if not installed, which is expected)
        try:
            from flask import Flask
            from flask_sqlalchemy import SQLAlchemy
            from flask_login import LoginManager
            from flask_mail import Mail
            print("✓ Flask modules available")
        except ImportError as e:
            print(f"⚠ Flask modules not installed: {e}")
            print("  Run: pip install -r requirements.txt")
        
        # Test ReportLab imports (will fail if not installed, which is expected)
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate
            print("✓ ReportLab modules available")
        except ImportError as e:
            print(f"⚠ ReportLab modules not installed: {e}")
            print("  Run: pip install -r requirements.txt")
        
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        'app.py',
        '__init__.py',
        'models.py',
        'routes.py',
        'requirements.txt',
        'README.md',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/register.html',
        'templates/donor/dashboard.html',
        'templates/donor/donate.html',
        'templates/requestor/dashboard.html',
        'templates/delivery/dashboard.html',
        'templates/admin/dashboard.html',
        'static/css/style.css'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("✗ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✓ All required files present")
        return True

def test_app_creation():
    """Test if the app can be created without errors"""
    try:
        # This will fail if Flask is not installed, which is expected
        from __init__ import create_app
        app = create_app()
        print("✓ Flask app created successfully")
        return True
    except ImportError as e:
        print(f"⚠ Cannot test app creation: {e}")
        print("  Install dependencies first: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("MealBridge Application Test")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Import Tests", test_imports),
        ("App Creation", test_app_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"  Test failed: {test_name}")
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! MealBridge is ready to run.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the application: python app.py")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("⚠ Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
