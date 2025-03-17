# Enhanced Devin Gradio UI Installation Guide

This guide explains how to install and set up the Enhanced Devin Gradio UI.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
cd XinobiAgent_Devin
```

2. Install the required dependencies:

```bash
pip install gradio matplotlib numpy psutil
```

3. Set up the Devin API key:

```bash
export DEVIN_API_KEY=your_api_key_here
```

Or you can provide it when running the UI.

## Running the UI

You can run the UI using one of the provided scripts:

```bash
# Using the run script
python enhanced_devin/ui/run_ui.py --share

# Using the launcher
python enhanced_devin/ui/launcher.py --share

# Using the test integration script
python enhanced_devin/ui/test_integration.py --share

# Using the public URL script
python run_gradio_ui_with_public_url.py

# Using the test script
python test_run_enhanced_devin_ui.py --share
```

Command line options:

- `--api-key`: API key for Devin API (can also be set via the `DEVIN_API_KEY` environment variable)
- `--port`: Port to run the UI on (default: 7860)
- `--host`: Host to run the UI on (default: 0.0.0.0)
- `--share`: Create a public URL using Gradio's sharing feature
- `--debug`: Enable debug mode

## Verifying the Installation

After running the UI, you should see output similar to:

```
Starting Enhanced Devin Gradio UI
Running on local URL:  http://0.0.0.0:7860
Running on public URL: https://xxx-xxx-xxx.gradio.live
```

You can access the UI by opening the provided URL in your web browser.

## Troubleshooting

If you encounter issues:

- Make sure you have installed all the required dependencies
- Check that you have set the Devin API key correctly
- Enable debug mode with the `--debug` flag
- Check the console output for error messages

## Next Steps

After installation, refer to the [Usage Guide](README_USAGE.md) for information on how to use the UI.
