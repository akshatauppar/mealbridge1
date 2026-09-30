#!/usr/bin/env python3
"""
Simple test to verify Flask application is working
"""

import requests
import time

def test_flask_app():
    """Test if the Flask application is responding"""
    try:
        # Wait a moment for the app to start
        time.sleep(2)
        
        # Test the homepage
        response = requests.get('http://localhost:5000', timeout=10)
        
        if response.status_code == 200:
            print("✅ Flask application is running successfully!")
            print(f"Status Code: {response.status_code}")
            print(f"Response Length: {len(response.text)} characters")
            
            # Check if the response contains expected content
            if "MealBridge" in response.text:
                print("✅ MealBridge content found in response")
            else:
                print("⚠️  MealBridge content not found in response")
                
            return True
        else:
            print(f"❌ Flask application returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask application")
        print("Make sure the application is running on http://localhost:5000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing Flask application: {e}")
        return False

if __name__ == "__main__":
    print("Testing MealBridge Flask Application...")
    print("=" * 50)
    
    success = test_flask_app()
    
    if success:
        print("\n🎉 Application is working correctly!")
        print("You can now open http://localhost:5000 in your browser")
    else:
        print("\n⚠️  Application test failed")
        print("Check the Flask application logs for errors")
