#!/bin/bash
# Script to create a Heroku app for note.com integration system

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
read -p "Enter a name for your Heroku app (leave blank for random name): " APP_NAME

# Create Heroku app
if [ -z "$APP_NAME" ]; then
    echo "Creating Heroku app with random name..."
    heroku create
    APP_NAME=$(heroku apps:info | grep "=== " | cut -d' ' -f2)
else
    echo "Creating Heroku app: $APP_NAME..."
    heroku create $APP_NAME
fi

# Add buildpacks
echo "Adding buildpacks..."
heroku buildpacks:add heroku/python --app $APP_NAME
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome --app $APP_NAME
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver --app $APP_NAME

# Set environment variables
echo "Setting environment variables..."

# USE_MOCK
read -p "Use mock mode? (True/False, default: True): " USE_MOCK
USE_MOCK=${USE_MOCK:-True}
heroku config:set USE_MOCK="$USE_MOCK" --app $APP_NAME

# NOTE_USERNAME and NOTE_PASSWORD (only if not using mock mode)
if [ "$USE_MOCK" != "True" ]; then
    read -p "Enter note.com username: " NOTE_USERNAME
    heroku config:set NOTE_USERNAME="$NOTE_USERNAME" --app $APP_NAME
    
    read -p "Enter note.com password: " NOTE_PASSWORD
    heroku config:set NOTE_PASSWORD="$NOTE_PASSWORD" --app $APP_NAME
fi

# OPENAI_API_KEY (only if not using mock mode)
if [ "$USE_MOCK" != "True" ]; then
    read -p "Enter OpenAI API key: " OPENAI_API_KEY
    heroku config:set OPENAI_API_KEY="$OPENAI_API_KEY" --app $APP_NAME
fi

# Set up git remote
echo "Setting up git remote..."
heroku git:remote --app $APP_NAME

# Deploy instructions
echo "App created successfully: $APP_NAME"
echo ""
echo "To deploy the application, run:"
echo "git push heroku master"
echo ""
echo "To open the application, run:"
echo "heroku open --app $APP_NAME"
