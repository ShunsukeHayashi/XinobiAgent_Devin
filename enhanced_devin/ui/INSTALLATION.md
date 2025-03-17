# Enhanced Devin UI Installation Guide

This guide explains how to install and set up the Enhanced Devin UI.

## Prerequisites

Before installing the Enhanced Devin UI, you need to have the following:

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
cd XinobiAgent_Devin
```

### 2. Install Dependencies

```bash
pip install gradio==5.21.0 aiohttp matplotlib numpy psutil
```

### 3. Set Up the Environment

```bash
# Optional: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Configure the API Key (Optional)

You can set the API key in the UI or as an environment variable:

```bash
export DEVIN_API_KEY=your_api_key_here
```

On Windows:

```bash
set DEVIN_API_KEY=your_api_key_here
```

## Running the UI

To run the UI, use the following command:

```bash
python run_simple_gradio_ui.py
```

To create a public URL that can be accessed from anywhere:

```bash
python run_simple_gradio_ui.py --share
```

## Command Line Options

The UI supports the following command line options:

- `--api-key`: API key for Devin API (can also be set via the `DEVIN_API_KEY` environment variable)
- `--port`: Port to run the UI on (default: 7860)
- `--host`: Host to run the UI on (default: 0.0.0.0)
- `--share`: Create a public URL using Gradio's sharing feature
- `--debug`: Enable debug mode

## Verifying the Installation

To verify that the installation was successful:

1. Run the UI with the `--debug` option:
   ```bash
   python run_simple_gradio_ui.py --debug
   ```
2. Open a web browser and navigate to `http://localhost:7860`
3. You should see the Enhanced Devin UI

## Troubleshooting

### Issue: Missing Dependencies

If you encounter errors about missing dependencies, try installing them manually:

```bash
pip install gradio==5.21.0
pip install aiohttp
pip install matplotlib
pip install numpy
pip install psutil
```

### Issue: Port Already in Use

If the port is already in use, try using a different port:

```bash
python run_simple_gradio_ui.py --port 8080
```

### Issue: Permission Denied

If you encounter permission issues, try running the command with sudo (on Linux/Mac):

```bash
sudo python run_simple_gradio_ui.py
```

Or run the command prompt as administrator (on Windows).

## Conclusion

You have successfully installed the Enhanced Devin UI. You can now use it to interact with the Enhanced Devin system.
