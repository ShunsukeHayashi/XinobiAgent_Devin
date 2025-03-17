# Enhanced Devin UI Installation Guide

This guide explains how to install and set up the Enhanced Devin UI.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
   cd XinobiAgent_Devin
   ```

2. **Install dependencies**:
   ```bash
   pip install gradio aiohttp matplotlib numpy psutil
   ```

## Running the UI

1. **Run the simplified UI**:
   ```bash
   python run_simple_gradio_ui.py
   ```

2. **Run with a public URL**:
   ```bash
   python run_simple_gradio_ui.py --share
   ```

3. **Run with debug mode**:
   ```bash
   python run_simple_gradio_ui.py --debug
   ```

4. **Run on a specific port**:
   ```bash
   python run_simple_gradio_ui.py --port 8080
   ```

## Configuration

No additional configuration is required for the mock mode. The UI will automatically use the mock API client.

## Troubleshooting

1. **Port already in use**:
   - Try using a different port:
     ```bash
     python run_simple_gradio_ui.py --port 8080
     ```

2. **UI not loading**:
   - Check that all dependencies are installed
   - Try running with debug mode to see more detailed error messages:
     ```bash
     python run_simple_gradio_ui.py --debug
     ```

3. **Module not found errors**:
   - Make sure you're running the script from the repository root directory
   - Check that all dependencies are installed
