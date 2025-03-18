# Secure Environment Variables Management for Heroku

This document provides best practices for managing sensitive environment variables in Heroku deployments.

## Security Best Practices

### 1. Never Commit Credentials to Git

- Never store credentials in your code or commit them to your repository
- Use environment variables or configuration files that are excluded from version control
- Add sensitive files to `.gitignore`

### 2. Use Heroku Config Vars

Heroku provides a secure way to store environment variables:

```bash
heroku config:set VARIABLE_NAME=value
```

These variables are:
- Encrypted at rest
- Available to your application at runtime
- Not visible in your application logs

### 3. Rotate Credentials Regularly

- Change passwords and API keys periodically
- Update Heroku config vars after rotation:

```bash
heroku config:set NOTE_PASSWORD=new_password
```

### 4. Limit Access to Environment Variables

- Restrict access to your Heroku dashboard
- Use Heroku Teams for role-based access control
- Consider using Heroku Pipelines to separate development and production environments

### 5. Use Environment-Specific Variables

For different environments (development, staging, production):

```bash
# Development
heroku config:set USE_MOCK=True --app your-dev-app

# Production
heroku config:set USE_MOCK=False --app your-prod-app
```

## Handling note.com Credentials

For the note.com integration system:

1. Store credentials as Heroku config vars:
   ```bash
   heroku config:set NOTE_USERNAME=your_username
   heroku config:set NOTE_PASSWORD=your_password
   ```

2. Consider using a dedicated account for automated posting

3. Enable two-factor authentication on your note.com account if available

4. Monitor account activity regularly

## OpenAI API Key Security

For the OpenAI API key:

1. Create a separate API key specifically for this application

2. Set usage limits on the API key

3. Store the key as a Heroku config var:
   ```bash
   heroku config:set OPENAI_API_KEY=your_api_key
   ```

4. Monitor API usage for unusual patterns

## Troubleshooting

If your application cannot access environment variables:

1. Verify that the variables are set:
   ```bash
   heroku config
   ```

2. Check that your application is reading the variables correctly by running a Python script:
   ```bash
   heroku run python -m check_env_vars
   ```

3. Restart your application after setting new variables:
   ```bash
   heroku restart
   ```
