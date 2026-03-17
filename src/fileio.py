"""File I/O operations for song finder."""

import csv
from pathlib import Path

from src.models import SongResult


def load_song_names(input_file: Path) -> list[str]:
    """Load and validate song names from input file.

    Args:
        input_file: Path to text file with song names (one per line).

    Returns:
        List of song names (stripped of whitespace).

    Raises:
        FileNotFoundError: If the input file doesn't exist.
        ValueError: If the file can't be read or contains no songs.
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Input file '{input_file}' not found")

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            song_names = [line.strip() for line in f if line.strip()]
    except Exception as e:
        raise ValueError(f"Error reading input file: {e}")

    if not song_names:
        raise ValueError("No song names found in input file")

    return song_names


def save_to_csv(results: list[SongResult], output_file: Path) -> None:
    """Save song results to a CSV file.

    Args:
        results: List of SongResult objects to save.
        output_file: Path to output CSV file.

    Raises:
        IOError: If writing to the file fails.
    """
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            # Derive headers from model field names
            fieldnames = list(SongResult.model_fields.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows([r.model_dump(exclude_none=True) for r in results])
        print(f"Results saved to: {output_file}")
    except Exception as e:
        raise IOError(f"Error writing output file: {e}")
