#!/bin/bash
# Script to set environment variables for note.com integration system on Heroku

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

# Set environment variables
echo "Setting environment variables for app: $APP_NAME"

# NOTE_USERNAME
read -p "Enter note.com username: " NOTE_USERNAME
heroku config:set NOTE_USERNAME="$NOTE_USERNAME" --app $APP_NAME

# NOTE_PASSWORD
read -p "Enter note.com password: " NOTE_PASSWORD
heroku config:set NOTE_PASSWORD="$NOTE_PASSWORD" --app $APP_NAME

# OPENAI_API_KEY
read -p "Enter OpenAI API key: " OPENAI_API_KEY
heroku config:set OPENAI_API_KEY="$OPENAI_API_KEY" --app $APP_NAME

# USE_MOCK
read -p "Use mock mode? (True/False, default: True): " USE_MOCK
USE_MOCK=${USE_MOCK:-True}
heroku config:set USE_MOCK="$USE_MOCK" --app $APP_NAME

# Verify environment variables
echo "Verifying environment variables..."
heroku config --app $APP_NAME

echo "Environment variables set successfully for app: $APP_NAME"
