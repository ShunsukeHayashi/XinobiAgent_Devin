# Developer Console Monitoring for Devin API

This directory contains scripts and documentation for monitoring Devin API interactions using the Chrome Developer Console.

## Overview

The Developer Console monitoring approach provides a way to analyze Devin API interactions without requiring a Chrome extension. It uses built-in Developer Tools features and custom scripts to capture and analyze API requests and responses.

## Contents

- `console_scripts/`: JavaScript scripts for monitoring API interactions
- `network_filters.md`: Documentation on filtering network requests
- `analysis_techniques.md`: Techniques for analyzing API interactions
- `monitoring_guide.md`: Step-by-step guide for setting up monitoring

## Getting Started

1. Open the Chrome Developer Console (F12 or Ctrl+Shift+I)
2. Navigate to the Network tab
3. Apply the filters described in `network_filters.md`
4. Copy and paste the scripts from `console_scripts/` into the Console tab
5. Start interacting with Devin to capture API interactions

## Related Resources

- Chrome extension for more advanced monitoring: See the `devin_chrome_extension/` directory
- Research findings: See the `research_findings/` directory
