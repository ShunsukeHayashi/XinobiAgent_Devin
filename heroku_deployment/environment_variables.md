# Heroku Environment Variables Configuration

This document explains how to configure environment variables for the note.com integration system on Heroku.

## Required Environment Variables

The application requires the following environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| NOTE_USERNAME | Your note.com username | Yes | None |
| NOTE_PASSWORD | Your note.com password | Yes | None |
| OPENAI_API_KEY | Your OpenAI API key | Yes | None |
| USE_MOCK | Whether to use mock data | No | True |
| PORT | Port for the web server | No | 8080 |

## Setting Environment Variables

### Using Heroku CLI

```bash
heroku config:set NOTE_USERNAME=your_username
heroku config:set NOTE_PASSWORD=your_password
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set USE_MOCK=True
```

### Using Heroku Dashboard

1. Go to the Heroku dashboard.
2. Select your application.
3. Click the "Settings" tab.
4. Under "Config Vars", click "Reveal Config Vars".
5. Add each environment variable and its value.
6. Click "Add" for each variable.

### Using app.json (for One-Click Deployment)

The `app.json` file in the repository root already includes the required environment variables for one-click deployment:

```json
{
  "env": {
    "NOTE_USERNAME": {
      "description": "Your note.com username",
      "required": false
    },
    "NOTE_PASSWORD": {
      "description": "Your note.com password",
      "required": false
    },
    "OPENAI_API_KEY": {
      "description": "Your OpenAI API key",
      "required": false
    },
    "USE_MOCK": {
      "description": "Whether to use mock data (True/False)",
      "value": "True",
      "required": false
    }
  }
}
```

## Viewing Environment Variables

To view the current environment variables:

```bash
heroku config
```

## Removing Environment Variables

To remove an environment variable:

```bash
heroku config:unset VARIABLE_NAME
```

## Security Considerations

- Environment variables are encrypted at rest.
- Never commit sensitive environment variables to your repository.
- Consider using Heroku's config vars for all sensitive information.
- For production deployments, use a secure password manager to store credentials.
