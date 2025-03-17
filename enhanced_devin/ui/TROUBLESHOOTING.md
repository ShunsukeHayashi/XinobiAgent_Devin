# Enhanced Devin UI Troubleshooting Guide

This guide provides solutions to common issues that may arise when using the Enhanced Devin UI.

## Installation Issues

### Issue: Missing Dependencies

**Symptoms:**
- Error messages about missing modules when starting the UI
- ImportError or ModuleNotFoundError exceptions

**Solution:**
Install the required dependencies manually:

```bash
pip install gradio==5.21.0
pip install aiohttp
pip install matplotlib
pip install numpy
pip install psutil
```

### Issue: Version Conflicts

**Symptoms:**
- Error messages about incompatible versions
- AttributeError or TypeError exceptions

**Solution:**
Create a fresh virtual environment and install the exact versions of the dependencies:

```bash
python -m venv fresh_venv
source fresh_venv/bin/activate  # On Windows: fresh_venv\Scripts\activate
pip install gradio==5.21.0 aiohttp matplotlib numpy psutil
```

## Startup Issues

### Issue: Port Already in Use

**Symptoms:**
- Error message: "Address already in use"
- UI fails to start

**Solution:**
Use a different port:

```bash
python run_simple_gradio_ui.py --port 8080
```

### Issue: Permission Denied

**Symptoms:**
- Error message: "Permission denied"
- UI fails to start

**Solution:**
Run the command with elevated privileges or choose a port number above 1024:

```bash
# On Linux/Mac
sudo python run_simple_gradio_ui.py

# Or use a higher port
python run_simple_gradio_ui.py --port 8080
```

## UI Issues

### Issue: UI Not Loading

**Symptoms:**
- Browser shows a blank page or loading spinner
- No error messages in the console

**Solution:**
1. Check if the UI is running by visiting `http://localhost:7860` (or the port you specified)
2. Try a different browser
3. Clear your browser cache and cookies
4. Restart the UI with the `--debug` flag to see more detailed logs:
   ```bash
   python run_simple_gradio_ui.py --debug
   ```

### Issue: Session Creation Fails

**Symptoms:**
- Error message when creating a session
- Session doesn't appear in the dropdown

**Solution:**
1. Check if the API key is set correctly (if using a real API)
2. Restart the UI
3. Check the logs for error messages

### Issue: Messages Not Sending

**Symptoms:**
- Messages don't appear in the chat history
- No response from the agent

**Solution:**
1. Check if a session is active
2. Try creating a new session
3. Check the logs for error messages
4. Restart the UI

## API Issues

### Issue: API Key Not Working

**Symptoms:**
- Error messages about authentication
- API requests failing

**Solution:**
1. Check if the API key is entered correctly
2. Try setting the API key as an environment variable:
   ```bash
   export DEVIN_API_KEY=your_api_key_here
   ```
3. For testing purposes, you can use the UI without an API key (it will use a mock API client)

### Issue: API Requests Timing Out

**Symptoms:**
- Error messages about timeouts
- Long delays when sending messages

**Solution:**
1. Check your internet connection
2. Try again later
3. For testing purposes, you can use the UI without an API key (it will use a mock API client)

## File Upload Issues

### Issue: File Upload Fails

**Symptoms:**
- Error message when uploading a file
- File doesn't appear in the UI

**Solution:**
1. Check if the file size is within limits (usually 200MB)
2. Try a smaller file
3. Check the file format (text files work best for testing)

## Public URL Issues

### Issue: Public URL Not Working

**Symptoms:**
- Public URL not generated
- Error when accessing the public URL

**Solution:**
1. Make sure you're using the `--share` flag:
   ```bash
   python run_simple_gradio_ui.py --share
   ```
2. Check your internet connection
3. Try again later
4. If using a corporate network, check if outbound connections are allowed

## Advanced Troubleshooting

### Checking Logs

For more detailed troubleshooting, check the logs:

```bash
python run_simple_gradio_ui.py --debug > ui_log.txt 2>&1
```

This will save the logs to a file called `ui_log.txt`.

### Debugging Network Issues

If you suspect network issues, you can use tools like `curl` to test API connectivity:

```bash
curl -v https://api.example.com/endpoint
```

### Reporting Issues

If you encounter an issue that isn't covered in this guide, please report it with the following information:

1. Steps to reproduce the issue
2. Error messages (if any)
3. Operating system and Python version
4. Logs from running the UI with the `--debug` flag

## Conclusion

Most issues with the Enhanced Devin UI can be resolved by checking dependencies, restarting the UI, or using the `--debug` flag to get more information. If you continue to experience issues, please report them as described above.
