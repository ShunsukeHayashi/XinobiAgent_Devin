# Heroku Deploy Button Setup

The "Deploy to Heroku" button in the README.md allows users to deploy the application to Heroku with a single click. This document explains how it works and how to customize it.

## How It Works

The Deploy to Heroku button uses the `app.json` file in the repository root to configure the application. When a user clicks the button, Heroku reads this file to determine:

1. Application name and description
2. Required buildpacks
3. Environment variables
4. Post-deployment scripts

## Customizing the Deployment

To customize the deployment, edit the `app.json` file. The current configuration includes:

- Python buildpack
- Google Chrome buildpack for Playwright
- ChromeDriver buildpack
- Environment variables for note.com credentials and OpenAI API key
- Post-deployment script to install Playwright browsers

## Button HTML

The button in the README.md is created with the following HTML:

```html
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
```

## Testing the Button

To test the button:

1. Push your changes to GitHub
2. Click the button in the README.md
3. Follow the Heroku deployment process
4. Verify that the application deploys correctly

## Troubleshooting

If the deployment fails:

1. Check the Heroku build logs
2. Verify that all required buildpacks are specified in `app.json`
3. Ensure that all required environment variables are defined
4. Check that the post-deployment script is correct
