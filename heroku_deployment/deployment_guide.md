# Heroku Deployment Guide

This guide provides comprehensive instructions for deploying the note.com integration system to Heroku.

## Deployment Methods

There are three ways to deploy the application to Heroku:

1. **One-Click Deployment**: Using the "Deploy to Heroku" button in the README.md file.
2. **Git Deployment**: Pushing the code to a Heroku git repository.
3. **Docker Deployment**: Using the Heroku Container Registry.

## One-Click Deployment

For detailed instructions on one-click deployment, see [One-Click Deployment Guide](./one_click_deploy.md).

## Git Deployment

### Prerequisites

- Heroku CLI installed
- Git installed
- Heroku account

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
   cd XinobiAgent_Devin
   ```

2. Login to Heroku:
   ```bash
   heroku login
   ```

3. Create a new Heroku app:
   ```bash
   heroku create note-integration-app
   ```

4. Add buildpacks:
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome
   heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver
   ```

5. Set environment variables:
   ```bash
   heroku config:set NOTE_USERNAME=your_username
   heroku config:set NOTE_PASSWORD=your_password
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set USE_MOCK=True
   ```

6. Deploy the application:
   ```bash
   git push heroku master
   ```

7. Open the application:
   ```bash
   heroku open
   ```

## Docker Deployment

### Prerequisites

- Heroku CLI installed
- Docker installed
- Heroku account

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
   cd XinobiAgent_Devin
   ```

2. Login to Heroku:
   ```bash
   heroku login
   ```

3. Create a new Heroku app:
   ```bash
   heroku create note-integration-app
   ```

4. Set the stack to container:
   ```bash
   heroku stack:set container
   ```

5. Set environment variables:
   ```bash
   heroku config:set NOTE_USERNAME=your_username
   heroku config:set NOTE_PASSWORD=your_password
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set USE_MOCK=True
   ```

6. Deploy the application:
   ```bash
   git push heroku master
   ```

7. Open the application:
   ```bash
   heroku open
   ```

## Post-Deployment

After deployment, you can:

- View logs: `heroku logs --tail`
- Run commands: `heroku run python -m playwright install`
- Scale dynos: `heroku ps:scale web=1`
- Add add-ons: `heroku addons:create papertrail`

## Troubleshooting

For common issues and solutions, see [Troubleshooting Guide](./troubleshooting.md).

## Environment Variables

For details on environment variables, see [Environment Variables Guide](./environment_variables.md).
