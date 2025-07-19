#!/usr/bin/env python
import sys
print(f"Python version: {sys.version}")
print("Testing imports...")

try:
    import flask
    print("✓ Flask imported")
except Exception as e:
    print(f"✗ Flask import failed: {e}")

try:
    import travel_aigent
    print("✓ travel_aigent imported")
except Exception as e:
    print(f"✗ travel_aigent import failed: {e}")

try:
    from travel_aigent import create_app
    print("✓ create_app imported")
except Exception as e:
    print(f"✗ create_app import failed: {e}")

try:
    import app
    print("✓ app module imported")
except Exception as e:
    print(f"✗ app module import failed: {e}")

try:
    app = create_app()
    print("✓ App created successfully")
except Exception as e:
    print(f"✗ App creation failed: {e}")

print("\nAll tests completed.")