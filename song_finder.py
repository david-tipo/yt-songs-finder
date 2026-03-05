#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pydantic",
#   "yt-dlp",
#   "tqdm",
# ]
# ///

import csv
import yt_dlp
import asyncio
import argparse
from pathlib import Path

from pydantic import BaseModel
from tqdm.asyncio import tqdm


DLP_PARAMS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": True,
    "socket_timeout": 15,
}


class SongResult(BaseModel):
    song_name: str
    youtube_url: str


async def get_song_id(song_name: str) -> str | None:
    with yt_dlp.YoutubeDL(DLP_PARAMS) as ydl:
        info = await asyncio.to_thread(
            ydl.extract_info,
            f"ytsearch1:{song_name}",
            download=False,
        )

        if info and "entries" in info and len(info["entries"]) > 0:
            return info["entries"][0]["id"]


def load_song_names(input_file: Path) -> list[str]:
    """Load and validate song names from input file.

    Raises:
        FileNotFoundError: if the input file doesn't exist
        ValueError: if the file can't be read or contains no songs
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


async def process_songs(song_names: list[str]) -> list[SongResult]:
    """Fetch song IDs concurrently and return list of SongResult models.

    Raises:
        Exception: propagates any error from get_song_id
    """
    song_ids = await tqdm.gather(
        *[get_song_id(song_name) for song_name in song_names],
        desc="Fetching songs",
        total=len(song_names),
    )

    return [
        SongResult(
            song_name=song_name,
            youtube_url=f"https://www.youtube.com/watch?v={song_id}"
            if song_id
            else "Not found",
        )
        for song_name, song_id in zip(song_names, song_ids)
    ]


def save_to_csv(results: list[SongResult], output_file: Path) -> None:
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            # derive headers from model field names
            fieldnames = list(SongResult.model_fields.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows([r.model_dump(exclude_none=True) for r in results])
        print(f"Results saved to: {output_file}")
    except Exception as e:
        raise IOError(f"Error writing output file: {e}")


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find YouTube URLs for songs from a text file"
    )
    parser.add_argument(
        "input_file", type=Path, help="Text file with song names (one per line)"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default="songs_urls.csv",
        help="CSV output file (default: songs_urls.csv)",
    )

    args = parser.parse_args()

    song_names = load_song_names(args.input_file)
    print(f"Found {len(song_names)} song(s) to process...")

    results = await process_songs(song_names)
    save_to_csv(results, args.output)


if __name__ == "__main__":
    asyncio.run(main())
