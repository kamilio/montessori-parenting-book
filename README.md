# Montessori Parenting Guide

A comprehensive guide for Montessori-inspired parenting during the toddler years (12-24 months).

## Quick Start

```bash
# Install all dependencies
make install

# Build the EPUB book
make build-epub

# Generate audio chapters (requires OpenAI API key in .env)
make generate-audio-chapters

# Create audiobook (M4B format)
make generate-audiobook
```

## Prerequisites

- Python 3.8+ (accessible as `python3`)
- macOS with Homebrew (for m4b-tool installation)
- OpenAI API key (for audio generation)

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
3. Install dependencies:
   ```bash
   make install
   ```

## Available Commands

### `make install`
Installs all Python dependencies and m4b-tool requirements (ffmpeg, php, composer).

### `make build-epub`
Builds an EPUB file from the markdown chapters in the `montesorri 12-15-months/chapters/` directory.

### `make generate-audio-chapters`
Generates MP3 audio files for each chapter using OpenAI's text-to-speech API. Audio files are saved to `montesorri 12-15-months/audio_chapters/`.

### `make generate-audiobook`
Creates an M4B audiobook file from the generated MP3 chapters. This command automatically runs `generate-audio-chapters` if needed.

### `make clean`
Removes generated EPUB and M4B files.

### `make help`
Shows all available make commands.

## Project Structure

```
.
├── Makefile                    # Build automation
├── requirements.txt            # Python dependencies
├── build_epub.py              # EPUB builder script
├── generate_audio.py          # Audio generation script
├── create_audiobook.py        # M4B audiobook creator
├── analyze_chapters.py        # Chapter length analyzer
└── montesorri 12-15-months/
    ├── chapters/              # Markdown chapter files
    ├── audio_chapters/        # Generated MP3 files
    └── planning/              # Book planning documents
```

## Manual Commands

If you prefer to run commands directly without make:

```bash
# Build EPUB
python3 build_epub.py

# Generate audio chapters
python3 generate_audio.py

# Create audiobook
python3 create_audiobook.py

# Analyze chapter lengths
python3 analyze_chapters.py
```

## Troubleshooting

- **Missing .env file**: Copy `.env.example` to `.env` and add your OpenAI API key
- **m4b-tool not found**: Run `make install` or manually install with `composer global require sandreas/m4b-tool`
- **Audio generation fails**: Check your OpenAI API key and ensure you have sufficient credits