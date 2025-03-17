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
   pip install gradio matplotlib numpy psutil
   ```

## Configuration

1. **Set up API key**:
   - Option 1: Set the `DEVIN_API_KEY` environment variable:
     ```bash
     export DEVIN_API_KEY=your_api_key
     ```
   - Option 2: Pass the API key as a command-line argument:
     ```bash
     python run_enhanced_devin_ui.py --api-key your_api_key
     ```

## Running the UI

1. **Run the UI with a public URL**:
   ```bash
   python run_enhanced_devin_ui.py
   ```

2. **Run the UI with debug mode**:
   ```bash
   python run_enhanced_devin_ui.py --debug
   ```

3. **Run the UI on a specific port**:
   ```bash
   python run_enhanced_devin_ui.py --port 8080
   ```

## Troubleshooting

1. **Port already in use**:
   - Try using a different port:
     ```bash
     python run_enhanced_devin_ui.py --port 8080
     ```

2. **API key not working**:
   - Make sure you have set the correct API key
   - Check that the API key has the necessary permissions

3. **UI not loading**:
   - Check that all dependencies are installed
   - Try running with debug mode to see more detailed error messages:
     ```bash
     python run_enhanced_devin_ui.py --debug
     ```
