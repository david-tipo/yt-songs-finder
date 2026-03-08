#!/bin/bash

# Setup Script for macOS
# Installs uv and ffmpeg if needed

echo
echo "========================================"
echo "  Setting up Song Finder dependencies"
echo "  (uv and ffmpeg installation)"
echo "========================================"
echo

# ---- Install uv ----------------------------------------------------

echo "Installing uv..."

curl -LsSf https://astral.sh/uv/install.sh | sh

if [ $? -ne 0 ]; then
    echo
    echo "Error: uv installation failed."
    echo "Please check your internet connection or install manually:"
    echo "https://astral.sh/uv"
else
    echo "========================================"
    echo "  uv installed successfully!"
    echo "========================================"
    echo
    echo "You may need to restart your terminal."
    echo
    echo "Verify installation with:"
    echo "  uv --version"
fi

# ---- Check for ffmpeg ----------------------------------------------

echo
echo "Checking for ffmpeg..."

if command -v ffmpeg >/dev/null 2>&1; then
    echo "ffmpeg is already installed."
else
    echo "ffmpeg not found."

    # Check if Homebrew exists
    if command -v brew >/dev/null 2>&1; then
        echo "Installing ffmpeg using Homebrew..."
        brew install ffmpeg
    else
        echo
        echo "Homebrew not found."
        echo "Install Homebrew first:"
        echo
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        echo
        echo "Then run:"
        echo "  brew install ffmpeg"
    fi
fi

echo
echo "Setup complete."