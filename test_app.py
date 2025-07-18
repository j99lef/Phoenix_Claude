#!/usr/bin/env python3
"""Quick test of Travel AiGent deployment"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set required environment variables
os.environ['FLASK_SECRET_KEY'] = 'test-secret-key-123456789'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'test123'

try:
    from travel_aigent import create_app
    
    print("✅ Creating Flask app...")
    app = create_app()
    
    print(f"✅ Template folder: {app.template_folder}")
    print(f"✅ Static folder: {app.static_folder}")
    print(f"✅ Templates exist: {os.path.exists(app.template_folder)}")
    print(f"✅ Login template: {os.path.exists(os.path.join(app.template_folder, 'login.html'))}")
    
    # Test routes
    with app.test_client() as client:
        response = client.get('/login')
        print(f"✅ Login route status: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 APP WORKS! Ready for deployment")
        else:
            print(f"❌ Login route failed: {response.data}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()