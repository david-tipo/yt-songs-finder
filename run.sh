#!/bin/bash
# Song Finder - Run with songs.txt

echo
echo "========================================"
echo "  Song Finder - Processing songs.txt"
echo "========================================"
echo

uv run --script song_finder.py songs.txt

echo
echo "========================================"
echo "  Processing complete!"
echo "========================================"
echo

read -p "Press Enter to exit..."