# Heroku Deployment Troubleshooting Guide

This guide provides solutions for common issues encountered when deploying the note.com integration system to Heroku.

## Common Issues and Solutions

### Application Crashes on Startup

**Symptoms**: The application crashes immediately after deployment, showing an H10 error in the logs.

**Possible Causes and Solutions**:

1. **Missing Environment Variables**:
   - Check that all required environment variables are set.
   - Use `heroku config` to verify.

2. **Buildpack Issues**:
   - Ensure all required buildpacks are added.
   - Check the build logs for buildpack-related errors.

3. **Port Configuration**:
   - Verify that the application is listening on the port specified by the `PORT` environment variable.
   - The `Procfile` should use `$PORT` for the web process.

### Playwright Browser Issues

**Symptoms**: The application fails to launch the browser for note.com authentication.

**Possible Causes and Solutions**:

1. **Missing Chrome Buildpack**:
   - Ensure the Chrome buildpack is added: `heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome`

2. **Missing ChromeDriver Buildpack**:
   - Ensure the ChromeDriver buildpack is added: `heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver`

3. **Playwright Installation**:
   - Run `heroku run python -m playwright install` to install Playwright browsers.
   - Run `heroku run python -m playwright install-deps` to install dependencies.

4. **Headless Mode**:
   - Ensure the application is using headless mode for browser automation.
   - Set `HEADLESS=True` in the environment variables.

### Memory Limit Exceeded

**Symptoms**: The application crashes with an R14 or R15 error in the logs.

**Possible Causes and Solutions**:

1. **Dyno Size**:
   - Upgrade to a larger dyno size: `heroku ps:resize web=standard-2x`

2. **Memory Leaks**:
   - Check for memory leaks in the application code.
   - Implement proper resource cleanup.

3. **Browser Memory Usage**:
   - Configure Playwright to use less memory.
   - Close browser instances after use.

### Slow Application Performance

**Symptoms**: The application is slow to respond or times out.

**Possible Causes and Solutions**:

1. **Dyno Size**:
   - Upgrade to a larger dyno size: `heroku ps:resize web=standard-2x`

2. **Concurrent Requests**:
   - Implement request queuing or rate limiting.
   - Scale the application horizontally: `heroku ps:scale web=2`

3. **Database Issues**:
   - Check database connection pool settings.
   - Optimize database queries.

### Deployment Fails

**Symptoms**: The deployment process fails with an error.

**Possible Causes and Solutions**:

1. **Git Issues**:
   - Ensure you're pushing to the correct remote: `git remote -v`
   - Try force pushing: `git push heroku master --force`

2. **Build Failures**:
   - Check the build logs for specific errors.
   - Ensure all dependencies are specified in `requirements.txt`.

3. **Large Repository**:
   - Remove large files or use Git LFS.
   - Add large files to `.slugignore`.

## Viewing Logs

To view the application logs:

```bash
heroku logs --tail
```

## Restarting the Application

To restart the application:

```bash
heroku restart
```

## Contacting Support

If you're unable to resolve the issue, contact Heroku support:

1. Go to the [Heroku Support Center](https://help.heroku.com/).
2. Click "Submit a Ticket".
3. Provide details about the issue, including error messages and steps to reproduce.
