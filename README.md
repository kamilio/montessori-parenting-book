# Montessori Parenting Guide

## Building EPUB

Install dependencies and generate EPUB:
```bash
pip install -r requirements.txt
python build_epub.py
```

## Generating Audio

1. Copy `.env.example` to `.env` and add your OpenAI API key
2. Generate audio for all chapters (only if content changed):
```bash
python generate_audio.py
```

## Creating Audiobook (M4B)

1. Install m4b-tool:
```bash
brew install ffmpeg php composer
composer global require sandreas/m4b-tool
```

2. Create M4B audiobook from generated MP3s:
```bash
python create_audiobook.py
```