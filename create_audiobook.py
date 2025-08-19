#!/usr/bin/env python3
"""
Create M4B audiobook from generated MP3 chapters using m4b-tool.
Generates chapters.txt from audio metadata and merges into audiobook.
"""

import os
import json
import subprocess

METADATA_FILE = "audio_metadata.json"
CHAPTERS_FILE = "chapters.txt"
AUDIO_DIR = "montesorri 12-15-months/audio"

def load_metadata():
    """Load audio metadata"""
    if not os.path.exists(METADATA_FILE):
        print(f"Error: {METADATA_FILE} not found. Run generate_audio.py first.")
        return None
    
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)

def format_duration(seconds):
    """Convert seconds to HH:MM:SS.000 format"""
    if seconds is None:
        return "00:00:00.000"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

def generate_chapters_file(metadata):
    """Generate chapters.txt file from metadata"""
    print("Generating chapters.txt...")
    
    # Sort chapters: introduction first, then chapters in order
    def sort_key(item):
        key = item[0]
        if key.startswith("introduction"):
            return "00-" + key
        elif key.startswith("chapter"):
            return "01-" + key
        else:
            return "02-" + key
    
    sorted_chapters = sorted(metadata.items(), key=sort_key)
    
    chapters = []
    current_time = 0.0
    
    for chapter_key, chapter_data in sorted_chapters:
        duration = chapter_data.get('duration_seconds', 0)
        
        # Get title from metadata if available, otherwise generate
        title = chapter_data.get('title', chapter_key.replace('-', ' ').title())
        
        chapters.append({
            'start_time': current_time,
            'title': title,
            'duration': duration
        })
        
        current_time += duration
    
    # Write chapters.txt file
    with open(CHAPTERS_FILE, 'w') as f:
        for chapter in chapters:
            timestamp = format_duration(chapter['start_time'])
            f.write(f"{timestamp} {chapter['title']}\n")
    
    print(f"Generated {CHAPTERS_FILE} with {len(chapters)} chapters")
    return len(chapters)

def get_mp3_files(metadata):
    """Get list of MP3 files in correct order"""
    # Use same sorting as generate_chapters_file
    def sort_key(item):
        key = item[0]
        if key.startswith("introduction"):
            return "00-" + key
        elif key.startswith("chapter"):
            return "01-" + key
        else:
            return "02-" + key
    
    sorted_chapters = sorted(metadata.items(), key=sort_key)
    
    mp3_files = []
    for chapter_key, chapter_data in sorted_chapters:
        audio_path = chapter_data.get('audio_path')
        if audio_path and os.path.exists(audio_path):
            mp3_files.append(audio_path)
    
    return mp3_files

def create_audiobook(metadata, output_file="montessori-guide.m4b"):
    """Create M4B audiobook using m4b-tool"""
    print("Creating M4B audiobook...")
    
    # Get MP3 files in order
    mp3_files = get_mp3_files(metadata)
    if not mp3_files:
        print("Error: No MP3 files found in metadata")
        return False
    
    # Check if cover exists
    cover_path = "montesorri 12-15-months/book-cover.png"
    
    # Build m4b-tool command (without --chapters-file for compatibility)
    cmd = [
        "m4b-tool", "merge",
        *mp3_files,
        "--output-file", output_file,
        "--name", "Montessori Parenting Guide (12-15 Months)",
        "--artist", "Montessori Parent",
        "--use-filenames-as-chapters"
    ]
    
    if os.path.exists(cover_path):
        cmd.extend(["--cover", cover_path])
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Successfully created audiobook: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating audiobook: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: m4b-tool not found. Install with: composer global require sandreas/m4b-tool")
        return False

def main():
    # Load metadata
    metadata = load_metadata()
    if not metadata:
        return
    
    # Generate chapters file
    chapter_count = generate_chapters_file(metadata)
    if chapter_count == 0:
        print("No chapters found in metadata")
        return
    
    # Create audiobook
    success = create_audiobook(metadata)
    if success:
        print("\nAudiobook creation complete!")
        print("Files created:")
        print(f"  - {CHAPTERS_FILE}")
        print(f"  - montessori-guide.m4b")
    else:
        print("Audiobook creation failed")

if __name__ == '__main__':
    main()