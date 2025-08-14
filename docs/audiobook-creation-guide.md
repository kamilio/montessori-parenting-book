# Quick Guide: Creating Audiobooks with m4b-tool

## Installation
```bash
brew install ffmpeg php composer  # macOS prerequisites
composer global require sandreas/m4b-tool
```

## Basic Usage with Custom Chapters
Create a `chapters.txt` file with timestamps and names:
```
00:00:00.000 Introduction to Montessori
00:15:30.000 Chapter 1: Your 12-15 Month Old
00:45:00.000 Chapter 2: Environment for New Walkers
01:10:00.000 Chapter 3: Activities and Development
```

Then merge with custom chapters:
```bash
m4b-tool merge "montesorri/*.mp3" --output-file="montessori-guide.m4b" \
  --name="Montessori Parenting Guide" --artist="Your Name" \
  --chapters-file="chapters.txt" --cover="cover.jpg"
```