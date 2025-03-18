# One-Click Deployment to Heroku

This document explains how to use the "Deploy to Heroku" button for quick deployment.

## Steps for One-Click Deployment

1. Click the "Deploy to Heroku" button in the README.md file:

   [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

2. You will be redirected to Heroku's deployment page.

3. If you're not logged in, you'll be prompted to log in to your Heroku account.

4. After logging in, you'll see a form with the following fields:
   - App name (you can customize this or leave it as the default)
   - Environment variables (NOTE_USERNAME, NOTE_PASSWORD, OPENAI_API_KEY, USE_MOCK)

5. Fill in the required environment variables:
   - NOTE_USERNAME: Your note.com username
   - NOTE_PASSWORD: Your note.com password
   - OPENAI_API_KEY: Your OpenAI API key
   - USE_MOCK: Set to "True" for testing or "False" for production

6. Click the "Deploy app" button.

7. Heroku will deploy the application with the specified configuration.

8. Once deployment is complete, click the "View" button to open the application.

## Troubleshooting

If you encounter issues during deployment:

1. Check that you've entered all required environment variables correctly.
2. Review the build logs for any errors.
3. If the application fails to start, check the application logs using the Heroku dashboard or CLI:
   ```bash
   heroku logs --tail --app your-app-name
   ```

## Post-Deployment Configuration

After deployment, you can modify the application settings:

1. Go to the Heroku dashboard.
2. Select your application.
3. Click the "Settings" tab.
4. Under "Config Vars", you can add, edit, or remove environment variables.
5. To update the application, push changes to the Heroku git repository:
   ```bash
   git push heroku master
   ```
