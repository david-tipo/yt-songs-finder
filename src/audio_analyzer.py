from pathlib import Path
import shutil

import librosa
from tqdm import tqdm as tqdm_sync


def calc_song_tempo(file_path: Path) -> float:
    """Calculate the tempo (BPM) of a song given its file path."""
    y, sr = librosa.load(file_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    
    return tempo[0]


def get_bpm_range_folder(bpm: float) -> str:
    """Determine BPM range folder name based on detected BPM value.

    Examples:
        85.5 BPM -> "080-100_BPM"
        125.0 BPM -> "120-140_BPM"
        180.0 BPM -> "180-200_BPM"
    """
    # Round down to nearest 20 BPM range
    lower = (int(bpm) // 20) * 20
    upper = lower + 20
    return f"{lower:03d}-{upper:03d}_BPM"


def organize_by_bpm(audio_file: Path, download_dir: Path) -> None:
    """Detect BPM and move audio file into appropriate BPM subfolder.

    If BPM detection fails, organizes into 'unknown_BPM' folder.
    """
    if not audio_file.exists():
        return

    try:
        bpm = calc_song_tempo(audio_file)
        bpm_folder = get_bpm_range_folder(bpm)
    except Exception as e:
        print(f"  Warning: Could not detect BPM for {audio_file.name}: {e}")
        bpm_folder = "unknown_BPM"

    target_dir = download_dir / bpm_folder
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / audio_file.name
    shutil.move(str(audio_file), str(target_path))


def organize_downloaded_songs(download_dir: Path) -> None:
    """Organize downloaded MP3 files by BPM into subfolders.

    Args:
        download_dir: Directory containing the downloaded MP3 files.
    """
    print("Analyzing and organizing songs by BPM...")
    # Find all downloaded MP3 files and organize them
    mp3_files = list(download_dir.glob("*.mp3"))
    
    # run detection+move in separate processes for speed
    def _process(file_path_str: str, download_dir_str: str) -> None:
        # helper executed in worker process
        audio_file = Path(file_path_str)
        download_dir_p = Path(download_dir_str)
        try:
            bpm = calc_song_tempo(audio_file)
            folder_name = get_bpm_range_folder(bpm)
        except Exception as e:
            print(f"  Warning: Could not detect BPM for {audio_file.name}: {e}")
            folder_name = "unknown_BPM"

        target_dir = download_dir_p / folder_name
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / audio_file.name
        shutil.move(str(audio_file), str(target_path))

    import concurrent.futures
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(_process, str(mp3), str(download_dir))
            for mp3 in mp3_files
        ]
        for _ in tqdm_sync(concurrent.futures.as_completed(futures),
                           desc="Organizing by BPM",
                           total=len(futures)):
            pass