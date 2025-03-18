# Heroku Deployment for note.com Integration System

This directory contains the necessary files for deploying the note.com integration system to Heroku.

## Deployment Steps

1. Create a Heroku account if you don't have one already
2. Install the Heroku CLI: `npm install -g heroku`
3. Login to Heroku: `heroku login`
4. Create a new Heroku app: `heroku create note-integration-app`
5. Set environment variables:
   ```
   heroku config:set NOTE_USERNAME=your_username
   heroku config:set NOTE_PASSWORD=your_password
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   ```
6. Deploy the app: `git push heroku master`
7. Open the app: `heroku open`

## Important Notes

- The app will run in mock mode by default on Heroku
- To run in production mode, set the environment variable `USE_MOCK=False`
- Playwright requires additional setup on Heroku, which is handled by the `heroku-buildpack-google-chrome` buildpack
