#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR"

if [ ! -f "app_ui.py" ]; then
    echo "Error: app_ui.py not found"
    exit 1
fi

sudo python app_ui.py