# Heroku Deploy Button Setup

This document explains how the "Deploy to Heroku" button is set up for the note.com integration system.

## How the Deploy Button Works

The "Deploy to Heroku" button is a simple way to deploy an application to Heroku directly from a GitHub repository. It uses the `app.json` file to configure the application.

## Button Markdown

The button is added to the README.md file using the following markdown:

```markdown
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
```

## app.json Configuration

The `app.json` file in the repository root configures the one-click deployment:

```json
{
  "name": "note.com Integration System",
  "description": "An autonomous agent system for posting SEO-optimized articles to note.com",
  "repository": "https://github.com/ShunsukeHayashi/XinobiAgent_Devin",
  "keywords": ["python", "gradio", "note.com", "seo", "content-generation"],
  "buildpacks": [
    {
      "url": "heroku/python"
    },
    {
      "url": "https://github.com/heroku/heroku-buildpack-google-chrome"
    },
    {
      "url": "https://github.com/heroku/heroku-buildpack-chromedriver"
    }
  ],
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
  },
  "scripts": {
    "postdeploy": "python -m playwright install"
  }
}
```

## Key Components

1. **name**: The name of the application.
2. **description**: A brief description of the application.
3. **repository**: The GitHub repository URL.
4. **keywords**: Tags for the application.
5. **buildpacks**: The buildpacks required for the application.
6. **env**: Environment variables for the application.
7. **scripts**: Scripts to run after deployment.

## Customization

To customize the deployment button:

1. Update the `app.json` file with your specific configuration.
2. Update the button URL in the README.md file to include your repository name:

```markdown
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ShunsukeHayashi/XinobiAgent_Devin)
```

## Testing the Button

To test the button:

1. Commit and push the `app.json` file to your repository.
2. Click the button in the README.md file.
3. Verify that the deployment process works as expected.
