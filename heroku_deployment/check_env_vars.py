#!/usr/bin/env python3
"""
Script to check if environment variables are set correctly in Heroku.
"""
import os
import sys

def check_env_vars():
    """Check if required environment variables are set."""
    required_vars = [
        "NOTE_USERNAME",
        "NOTE_PASSWORD",
        "OPENAI_API_KEY"
    ]
    
    optional_vars = [
        "USE_MOCK",
        "PORT"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All required environment variables are set:")
    for var in required_vars:
        # Print only the first few characters of sensitive variables
        if var in ["NOTE_PASSWORD", "OPENAI_API_KEY"]:
            value = os.environ.get(var)
            masked_value = value[:3] + "*" * (len(value) - 3) if value else ""
            print(f"  - {var}: {masked_value}")
        else:
            print(f"  - {var}: {os.environ.get(var)}")
    
    print("\nOptional environment variables:")
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            print(f"  - {var}: {value}")
        else:
            print(f"  - {var}: Not set (will use default)")
    
    return True

if __name__ == "__main__":
    success = check_env_vars()
    sys.exit(0 if success else 1)
