# Heroku Deployment Guide for note.com Integration System

This guide provides step-by-step instructions for deploying the note.com integration system to Heroku.

## Prerequisites

- Heroku account
- Heroku CLI installed
- Git installed

## Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Create a new Heroku app

```bash
heroku create note-integration-app
```

### 3. Add Buildpacks

```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver
```

### 4. Set Environment Variables

```bash
heroku config:set NOTE_USERNAME=your_username
heroku config:set NOTE_PASSWORD=your_password
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set USE_MOCK=True
```

### 5. Deploy the Application

```bash
git push heroku master
```

### 6. Open the Application

```bash
heroku open
```

## Using Docker Deployment (Alternative)

Heroku also supports Docker-based deployments using the `heroku.yml` file:

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

### Logs

Check the logs for any errors:

```bash
heroku logs --tail
```

## One-Click Deployment

You can also use the "Deploy to Heroku" button in the README.md file for one-click deployment.

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
