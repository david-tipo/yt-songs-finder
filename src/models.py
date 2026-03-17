"""Data models for song finder."""

from pydantic import BaseModel


class SongResult(BaseModel):
    """Result model for a song search."""
    song_name: str
    youtube_url: str | None = None
