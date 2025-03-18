# One-Click Deployment to Heroku

This guide provides instructions for deploying the note.com integration system to Heroku using the "Deploy to Heroku" button.

## Prerequisites

- Heroku account
- OpenAI API key (if not using mock mode)
- note.com account (if not using mock mode)

## Deployment Steps

1. Click the "Deploy to Heroku" button in the README.md file.

2. Fill in the required information:
   - App name: Choose a unique name for your application
   - Region: Choose the region closest to you
   - Environment variables:
     - NOTE_USERNAME: Your note.com username
     - NOTE_PASSWORD: Your note.com password
     - OPENAI_API_KEY: Your OpenAI API key
     - USE_MOCK: Set to "True" for testing without actual API calls

3. Click "Deploy App".

4. Wait for the deployment to complete.

5. Click "View" to open the application.

## Post-Deployment

After deployment, you can:

- View logs: `heroku logs --tail --app your-app-name`
- Run commands: `heroku run python -m playwright install --app your-app-name`
- Scale dynos: `heroku ps:scale web=1 --app your-app-name`
- Add add-ons: `heroku addons:create papertrail --app your-app-name`

## Troubleshooting

For common issues and solutions, see [Troubleshooting Guide](./troubleshooting.md).

## Environment Variables

For details on environment variables, see [Environment Variables Guide](./environment_variables.md).
