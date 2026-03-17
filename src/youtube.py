"""YouTube search and audio download functionality."""

import asyncio
from pathlib import Path

import yt_dlp
from tqdm.asyncio import tqdm

from src.config import DLP_PARAMS
from src.models import SongResult


async def get_song_id(song_name: str) -> str | None:
    """Search for a song on YouTube and return the video ID.
    
    Args:
        song_name: The name of the song to search for.
        
    Returns:
        The YouTube video ID if found, None otherwise.
    """
    with yt_dlp.YoutubeDL(DLP_PARAMS) as ydl:
        info = await asyncio.to_thread(
            ydl.extract_info,
            f"ytsearch1:{song_name}",
            download=False,
        )

        if info and "entries" in info and len(info["entries"]) > 0:
            return info["entries"][0]["id"]


async def process_songs(song_names: list[str]) -> list[SongResult]:
    """Fetch song IDs concurrently and return list of SongResult models.

    Args:
        song_names: List of song names to process.
        
    Returns:
        List of SongResult objects with YouTube URLs.
        
    Raises:
        Exception: Propagates any error from get_song_id.
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
            else None,
        )
        for song_name, song_id in zip(song_names, song_ids)
    ]


async def download_audio(url: str, download_dir: Path, quality: str) -> None:
    """Download audio from a YouTube URL as MP3 into the given directory.

    Args:
        url: YouTube URL to download from.
        download_dir: Directory where MP3 file will be saved.
        quality: Preferred bitrate for MP3 (e.g. "192" or "320").

    This runs in a thread to avoid blocking the event loop.
    """
    params = {
        **DLP_PARAMS,
        "format": "bestaudio/best",
        "outtmpl": str(download_dir / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            }
        ],
    }

    def _download():
        with yt_dlp.YoutubeDL(params) as ydl:
            ydl.download([url])

    await asyncio.to_thread(_download)


async def download_songs(
    songs: list[SongResult], download_dir: Path, quality: str
) -> None:
    """Download all songs with valid URLs concurrently.

    Args:
        songs: List of SongResult objects.
        download_dir: Directory where MP3 files will be saved.
        quality: Preferred bitrate for MP3 conversion.
    """
    tasks = []
    for song in songs:
        if song.youtube_url:
            tasks.append(download_audio(song.youtube_url, download_dir, quality))

    if tasks:
        await tqdm.gather(*tasks, desc="Downloading songs", total=len(tasks))
    else:
        print("No valid YouTube URLs found to download.")
