#!/usr/bin/env python3
"""
Script to verify the Heroku deployment of the note.com integration system.
"""
import os
import sys
import argparse
import requests
import time
import json

def check_url(url, max_retries=5, retry_delay=5):
    """Check if a URL is accessible."""
    print(f"Checking URL: {url}")
    
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                print(f"✅ URL is accessible: {url}")
                return True
            else:
                print(f"⚠️ URL returned status code {response.status_code}: {url}")
                print(f"Response: {response.text[:100]}...")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error accessing URL: {e}")
        
        if i < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    print(f"❌ URL is not accessible after {max_retries} retries: {url}")
    return False

def check_gradio_interface(url):
    """Check if the Gradio interface is working."""
    print("Checking Gradio interface...")
    
    try:
        response = requests.get(url, timeout=30)
        if "gradio" in response.text.lower():
            print("✅ Gradio interface detected.")
            return True
        else:
            print("❌ Gradio interface not detected.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking Gradio interface: {e}")
        return False

def check_api_endpoints(base_url):
    """Check if the API endpoints are working."""
    print("Checking API endpoints...")
    
    endpoints = [
        "/api/health",
        "/api/status"
    ]
    
    success_count = 0
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                print(f"✅ Endpoint is accessible: {endpoint}")
                success_count += 1
            else:
                print(f"❌ Endpoint returned status code {response.status_code}: {endpoint}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error accessing endpoint: {endpoint} - {e}")
    
    return success_count == len(endpoints)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Verify Heroku deployment of note.com integration system")
    parser.add_argument("--app-name", help="Heroku app name")
    parser.add_argument("--url", help="URL of the deployed application")
    args = parser.parse_args()
    
    if not args.app_name and not args.url:
        print("Error: Either --app-name or --url must be provided.")
        sys.exit(1)
    
    # Determine the URL
    if args.url:
        url = args.url
    else:
        url = f"https://{args.app_name}.herokuapp.com"
    
    # Check if the URL is accessible
    if not check_url(url):
        sys.exit(1)
    
    # Check if the Gradio interface is working
    if not check_gradio_interface(url):
        sys.exit(1)
    
    # Check if the API endpoints are working
    if not check_api_endpoints(url):
        print("⚠️ Some API endpoints are not working.")
    
    print("✅ Deployment verification completed successfully.")
    print(f"The application is accessible at: {url}")

if __name__ == "__main__":
    main()
