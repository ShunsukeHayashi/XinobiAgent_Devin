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

# Get app name from user or use default
read -p "Enter app name (default: note-integration-app): " APP_NAME
APP_NAME=${APP_NAME:-note-integration-app}

# Create Heroku app
echo "Creating Heroku app: $APP_NAME"
heroku create $APP_NAME

# Add buildpacks
echo "Adding buildpacks..."
heroku buildpacks:add heroku/python --app $APP_NAME
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome --app $APP_NAME
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver --app $APP_NAME

# Set environment variables
echo "Setting environment variables..."
read -p "Enter note.com username: " NOTE_USERNAME
read -p "Enter note.com password: " NOTE_PASSWORD
read -p "Enter OpenAI API key: " OPENAI_API_KEY
read -p "Use mock mode? (True/False, default: True): " USE_MOCK
USE_MOCK=${USE_MOCK:-True}

heroku config:set NOTE_USERNAME="$NOTE_USERNAME" --app $APP_NAME
heroku config:set NOTE_PASSWORD="$NOTE_PASSWORD" --app $APP_NAME
heroku config:set OPENAI_API_KEY="$OPENAI_API_KEY" --app $APP_NAME
heroku config:set USE_MOCK="$USE_MOCK" --app $APP_NAME

# Set remote
echo "Setting git remote..."
git remote add heroku https://git.heroku.com/$APP_NAME.git

echo "Heroku app created successfully: $APP_NAME"
echo "To deploy the application, run: git push heroku master"
echo "To open the application, run: heroku open --app $APP_NAME"
