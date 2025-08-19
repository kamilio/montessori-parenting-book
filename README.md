# Montessori Parenting Guide

A comprehensive guide for Montessori-inspired parenting during the toddler years (12-24 months).

## Setup

1. Copy `.env.example` to `.env` and add your OpenAI API key
2. Run `make install`

## Commands

- `make build-epub` - Build EPUB from markdown chapters
- `make generate-audio-chapters` - Generate MP3 audio files
- `make generate-audiobook` - Create M4B audiobook
- `make clean` - Remove generated files
- `make help` - Show all commands

## Audio Generation

### Process all chapters (default)
```bash
python3 generate_audio.py
# Processes all .md files in montesorri 12-15-months/chapters/
# Outputs to montesorri 12-15-months/chapters/audio/
```

### Process blinkist files
```bash
python3 generate_audio.py --blinkist
# Processes all .md files in montesorri 12-15-months/blinkist/
# Outputs to montesorri 12-15-months/blinkist/audio/
```

### Process single file
```bash
python3 generate_audio.py path/to/file.md
# Processes the specified file
# Outputs to same directory as input file in audio/ subdirectory
```