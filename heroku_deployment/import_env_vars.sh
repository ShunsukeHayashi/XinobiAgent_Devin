#!/bin/bash
# Script to import environment variables from .env file to Heroku

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI is not installed. Please install it first."
    echo "Visit https://devcenter.heroku.com/articles/heroku-cli for installation instructions."
    exit 1
fi

# Check if user is logged in to Heroku
heroku whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "You are not logged in to Heroku. Please login first."
    heroku login
fi

# Get app name from user
read -p "Enter Heroku app name: " APP_NAME

# Check if app exists
heroku apps:info --app $APP_NAME &> /dev/null
if [ $? -ne 0 ]; then
    echo "App '$APP_NAME' does not exist. Please create it first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo ".env file not found. Please create it first."
    echo "You can use env_var_template.env as a template."
    exit 1
fi

# Import environment variables from .env file
echo "Importing environment variables from .env file to app: $APP_NAME"
while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip comments and empty lines
    if [[ $line =~ ^#.*$ ]] || [[ -z $line ]]; then
        continue
    fi
    
    # Extract variable name and value
    var_name=$(echo "$line" | cut -d= -f1)
    var_value=$(echo "$line" | cut -d= -f2-)
    
    # Set environment variable in Heroku
    echo "Setting $var_name..."
    heroku config:set "$var_name=$var_value" --app $APP_NAME
done < .env

# Verify environment variables
echo "Verifying environment variables..."
heroku config --app $APP_NAME

echo "Environment variables imported successfully for app: $APP_NAME"
