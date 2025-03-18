#!/usr/bin/env python3
"""
Script to deploy the note.com integration system to Heroku.
"""
import os
import sys
import subprocess
import argparse
import time

def run_command(command, check=True):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e.stderr}")
        if check:
            sys.exit(1)
        return None

def check_heroku_cli():
    """Check if Heroku CLI is installed."""
    print("Checking if Heroku CLI is installed...")
    try:
        run_command("heroku --version")
        print("✅ Heroku CLI is installed.")
        return True
    except Exception:
        print("❌ Heroku CLI is not installed.")
        print("Please install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
        return False

def check_heroku_login():
    """Check if user is logged in to Heroku."""
    print("Checking if user is logged in to Heroku...")
    try:
        run_command("heroku whoami", check=False)
        print("✅ User is logged in to Heroku.")
        return True
    except Exception:
        print("❌ User is not logged in to Heroku.")
        print("Please login to Heroku: heroku login")
        return False

def create_heroku_app(app_name):
    """Create a new Heroku app."""
    print(f"Creating Heroku app: {app_name}...")
    try:
        run_command(f"heroku create {app_name}")
        print(f"✅ Heroku app created: {app_name}")
        return True
    except Exception:
        print(f"❌ Failed to create Heroku app: {app_name}")
        return False

def add_buildpacks(app_name):
    """Add required buildpacks to the Heroku app."""
    print("Adding buildpacks...")
    buildpacks = [
        "heroku/python",
        "https://github.com/heroku/heroku-buildpack-google-chrome",
        "https://github.com/heroku/heroku-buildpack-chromedriver"
    ]
    
    for buildpack in buildpacks:
        try:
            run_command(f"heroku buildpacks:add {buildpack} --app {app_name}")
            print(f"✅ Added buildpack: {buildpack}")
        except Exception:
            print(f"❌ Failed to add buildpack: {buildpack}")
            return False
    
    return True

def set_environment_variables(app_name, env_vars):
    """Set environment variables for the Heroku app."""
    print("Setting environment variables...")
    for key, value in env_vars.items():
        try:
            run_command(f"heroku config:set {key}={value} --app {app_name}")
            print(f"✅ Set environment variable: {key}")
        except Exception:
            print(f"❌ Failed to set environment variable: {key}")
            return False
    
    return True

def deploy_to_heroku(app_name):
    """Deploy the application to Heroku."""
    print("Deploying to Heroku...")
    try:
        run_command(f"git push https://git.heroku.com/{app_name}.git HEAD:master")
        print("✅ Deployed to Heroku.")
        return True
    except Exception:
        print("❌ Failed to deploy to Heroku.")
        return False

def check_deployment(app_name):
    """Check if the deployment was successful."""
    print("Checking deployment...")
    try:
        logs = run_command(f"heroku logs --tail --app {app_name}", check=False)
        if "State changed from starting to up" in logs:
            print("✅ Deployment successful.")
            return True
        else:
            print("⚠️ Deployment status unclear. Check logs for details.")
            return False
    except Exception:
        print("❌ Failed to check deployment status.")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Deploy note.com integration system to Heroku")
    parser.add_argument("--app-name", default="note-integration-app", help="Heroku app name")
    parser.add_argument("--use-mock", action="store_true", help="Use mock data")
    parser.add_argument("--note-username", help="note.com username")
    parser.add_argument("--note-password", help="note.com password")
    parser.add_argument("--openai-api-key", help="OpenAI API key")
    args = parser.parse_args()
    
    # Check prerequisites
    if not check_heroku_cli():
        return
    
    if not check_heroku_login():
        return
    
    # Create Heroku app
    if not create_heroku_app(args.app_name):
        return
    
    # Add buildpacks
    if not add_buildpacks(args.app_name):
        return
    
    # Set environment variables
    env_vars = {
        "USE_MOCK": "True" if args.use_mock else "False"
    }
    
    if args.note_username:
        env_vars["NOTE_USERNAME"] = args.note_username
    
    if args.note_password:
        env_vars["NOTE_PASSWORD"] = args.note_password
    
    if args.openai_api_key:
        env_vars["OPENAI_API_KEY"] = args.openai_api_key
    
    if not set_environment_variables(args.app_name, env_vars):
        return
    
    # Deploy to Heroku
    if not deploy_to_heroku(args.app_name):
        return
    
    # Check deployment
    if not check_deployment(args.app_name):
        return
    
    # Open the application
    print(f"Opening the application: https://{args.app_name}.herokuapp.com")
    run_command(f"heroku open --app {args.app_name}")

if __name__ == "__main__":
    main()
