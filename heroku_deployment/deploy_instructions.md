# Heroku Deployment Instructions for note.com Integration System

This document provides step-by-step instructions for deploying the note.com integration system to Heroku.

## Prerequisites

- Heroku account
- Heroku CLI installed locally

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
cd XinobiAgent_Devin
```

### 2. Login to Heroku

```bash
heroku login
```

### 3. Create a New Heroku App

```bash
heroku create note-integration-app
```

### 4. Add Buildpacks

The application requires several buildpacks for proper functionality:

```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver
```

### 5. Configure Environment Variables

Set the necessary environment variables for the application:

```bash
heroku config:set NOTE_USERNAME=your_username
heroku config:set NOTE_PASSWORD=your_password
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set USE_MOCK=True
```

For production use, set `USE_MOCK=False` once you've confirmed everything works correctly.

### 6. Deploy the Application

Push the code to Heroku:

```bash
git push heroku master
```

### 7. Open the Application

```bash
heroku open
```

## Alternative: One-Click Deployment

You can also use the "Deploy to Heroku" button in the README.md file for one-click deployment:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Docker Deployment (Alternative)

Heroku also supports Docker-based deployments:

```bash
heroku stack:set container
git push heroku master
```

## Troubleshooting

### Playwright Issues

If you encounter issues with Playwright, you can try:

```bash
heroku run python -m playwright install
heroku run python -m playwright install-deps
```

### Viewing Logs

Check the logs for any errors:

```bash
heroku logs --tail
```
