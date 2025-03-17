# Enhanced Devin UI Troubleshooting Guide

This guide provides solutions to common issues that may arise when using the Enhanced Devin UI.

## Installation Issues

### Missing Dependencies

**Issue**: Error messages about missing dependencies when running the UI.

**Solution**: Install the required dependencies using pip:
```bash
pip install gradio aiohttp matplotlib numpy psutil
```

### Port Already in Use

**Issue**: Error message about the port already being in use when starting the UI.

**Solution**: Use a different port:
```bash
python run_simple_gradio_ui.py --port 8080
```

## UI Issues

### UI Not Loading

**Issue**: The UI does not load or displays an error message.

**Solution**:
1. Check that all dependencies are installed
2. Try running with debug mode to see more detailed error messages:
```bash
python run_simple_gradio_ui.py --debug
```

### Session Creation Issues

**Issue**: Unable to create a session or error message when creating a session.

**Solution**:
1. Make sure you've entered a valid session name
2. Check the console for error messages
3. Try restarting the UI

### Message Sending Issues

**Issue**: Unable to send messages or error message when sending messages.

**Solution**:
1. Make sure you've created a session first
2. Check that your message is not empty
3. Check the console for error messages

### Tool Execution Issues

**Issue**: Unable to execute tools or error message when executing tools.

**Solution**:
1. Make sure you've created a session first
2. Check that your parameters are valid JSON
3. Verify that the tool name is correct
4. Check the console for error messages

## API Issues

### API Key Issues

**Issue**: Error message about missing or invalid API key.

**Solution**:
1. The UI is running in mock mode, which does not require an API key
2. If you want to use the real API, set the API key using the environment variable:
```bash
export DEVIN_API_KEY=your_api_key
```
3. Or pass the API key as a command-line argument:
```bash
python run_simple_gradio_ui.py --api-key your_api_key
```

### API Connection Issues

**Issue**: Error message about unable to connect to the API.

**Solution**:
1. Check your internet connection
2. Verify that the API is available
3. Check that your API key is valid
4. Try running in mock mode for testing:
```bash
python run_simple_gradio_ui.py
```

## Other Issues

### UI Crashes

**Issue**: The UI crashes or stops responding.

**Solution**:
1. Check the console for error messages
2. Try running with debug mode to see more detailed error messages:
```bash
python run_simple_gradio_ui.py --debug
```
3. Restart the UI

### Public URL Issues

**Issue**: Unable to access the UI via the public URL.

**Solution**:
1. Make sure you've used the `--share` option when starting the UI:
```bash
python run_simple_gradio_ui.py --share
```
2. Check that the public URL is valid
3. Try accessing the UI via localhost:
```
http://localhost:7860
```
