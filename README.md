# Song Finder with yt-dlp

A fast, async Python program that reads song names from a text file and outputs their YouTube URLs in CSV format.

## Installation

### Using uv (Recommended)

```bash
uv sync
```

### Using pip

```bash
pip install yt-dlp pydantic
```

## Usage

```bash
uv run song_finder.py <input_file> [-o OUTPUT_FILE]
```

### Arguments

- `input_file` (required): Path to a text file with song names, one per line
- `-o, --output` (optional): Output CSV file path. Defaults to `songs_urls.csv`

## Examples

1. Create an input file with song names:

```
Pump Up The Jam - Technotronic
Never Gonna Give You Up - Rick Astley
Bohemian Rhapsody - Queen
```

2. Run the program:

```bash
# Using default output filename (songs_urls.csv)
uv run song_finder.py songs.txt

# Specify custom output file
uv run song_finder.py songs.txt -o my_playlist.csv
```

3. The output CSV will contain two columns:

```
song_name,youtube_url
Pump Up The Jam - Technotronic,https://www.youtube.com/watch?v=9EcjWd-O4jI
Never Gonna Give You Up - Rick Astley,https://www.youtube.com/watch?v=dQw4w9WgXcQ
Bohemian Rhapsody - Queen,https://www.youtube.com/watch?v=fJ9rUzIMt7o
```

## How It Works

1. **Load Songs**: Reads and validates song names from the input file
2. **Search Concurrently**: Uses async/await to search YouTube for all songs simultaneously
3. **Extract URLs**: Gets the YouTube video ID from the first search result for each song
4. **Export Results**: Writes the results to a CSV file using Pydantic models

## Configuration

The following parameters can be modified in the `DLP_PARAMS` dictionary:

- `socket_timeout`: Timeout in seconds for network requests (default: 15)
- `quiet`: Suppress yt-dlp output (default: True)
- `no_warnings`: Suppress warnings (default: True)
- `extract_flat`: Only extract metadata without downloading (default: True)

## Error Handling

The program provides clear error messages for common issues:

- **FileNotFoundError**: Input file doesn't exist
- **ValueError**: No valid song names found in input file
- **IOError**: Failed to write output CSV file
- **Other exceptions**: General errors during YouTube searches (returns "Not found" for those songs)

## Performance

With concurrent processing, the program can search for 100 songs in roughly the time it takes to search for one song sequentially. Performance depends on:

- Internet connection speed
- YouTube API availability
- Number of songs to process

## License

MIT
