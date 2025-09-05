# CodeClip

A utility tool that automatically extracts verification codes from SMS messages and copies them to your clipboard.

## Features

- Monitors incoming SMS messages on macOS
- Automatically extracts verification codes (4-6 digit numbers)
- Copies extracted codes to clipboard for easy pasting
- Runs silently in the background

## Requirements

- macOS (requires access to the Messages database)
- iCloud Message sync enabled between iPhone and Mac (Messages must appear on your Mac)
- Python 3.6+
- Full Disk Access permission for the Terminal/application running the script

## Installation

1. Clone this repository
2. Make sure you have Python 3.6+ installed
3. Enable iCloud Message sync on your iPhone and Mac:
   - On iPhone: Go to Settings > [Your Name] > iCloud > Messages (turn on)
   - On Mac: Open Messages app > Preferences > iMessage > Enable "Enable Messages in iCloud"
4. Grant Full Disk Access permission to Terminal (or your preferred terminal app):
   - Open System Preferences > Security & Privacy > Privacy
   - Select "Full Disk Access" from the sidebar
   - Click the "+" button and add Terminal (or your preferred terminal app)
   - Ensure the checkbox next to the added application is checked

## Usage

### Starting the Service

To start the service in the background:

```bash
./start.sh
```

This script will:
- Check for necessary files
- Create a virtual environment if needed
- Install required dependencies
- Start the service in the background
- Display the process ID

### Stopping the Service

To stop the service:

```bash
./stop.sh
```

This script will find and terminate the running process.

## How It Works

The application monitors the macOS Messages database for new incoming messages containing numeric codes. When a verification code is detected, it's automatically copied to your clipboard, ready to be pasted wherever needed.

## Troubleshooting

If you encounter permission issues, ensure that:
- Terminal has Full Disk Access permission
- The scripts have execution permission (`chmod +x *.sh`)

For other issues, check the error messages displayed by the scripts. 