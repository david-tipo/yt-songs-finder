import asyncio
import argparse
from pathlib import Path
from datetime import datetime
from src.fileio import load_song_names, save_to_csv
from src.youtube import process_songs, download_songs
from src.audio_analyzer import organize_downloaded_songs

def generate_dir_path() -> Path:
    """Generate a directory path based on the current timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return Path("artifacts") / timestamp


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

    parser.add_argument(
        "-d",
        "--download-dir",
        type=Path,
        default=None,
        help="Folder where .mp3 files will be saved (if omitted, no download)",
    )

    parser.add_argument(
        "-q",
        "--quality",
        type=str,
        default="320",
        help="Preferred MP3 quality in kbps (passed to ffmpeg, e.g. 128, 192, 320).",
    )

    args = parser.parse_args()

    song_names = load_song_names(args.input_file)
    print(f"Found {len(song_names)} song(s) to process...")

    results = await process_songs(song_names)
    save_to_csv(results, args.output)

    # Ensure download directory exists
    artifacts_dir = args.download_dir or generate_dir_path()
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    await download_songs(results, artifacts_dir, args.quality)
    
    # Organize downloaded songs by BPM
    organize_downloaded_songs(artifacts_dir)

    


if __name__ == "__main__":
    asyncio.run(main())
