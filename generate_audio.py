#!/usr/bin/env python3
"""
Audio generation script for Montessori chapters with metadata tracking.
Only generates audio if chapter content has changed since last generation.
"""

import os
import sys
import json
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from mutagen.mp3 import MP3

# Load environment variables
load_dotenv()

METADATA_FILE = "audio_metadata.json"

def get_file_hash(file_path):
    """Calculate MD5 hash of file content"""
    with open(file_path, 'rb') as f:
        content = f.read()
    return hashlib.md5(content).hexdigest()

def load_metadata():
    """Load existing metadata or create empty dict"""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    """Save metadata to file"""
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

def get_mp3_duration(file_path):
    """Get duration of MP3 file in seconds"""
    try:
        audio = MP3(file_path)
        return audio.info.length
    except:
        return None

def generate_audio(file_path):
    """Generate audio from text file using OpenAI/ElevenLabs"""
    print(f"Generating audio for: {file_path}")
    
    # Read document content
    with open(file_path, 'r', encoding='utf-8') as f:
        document_content = f.read()
    
    # Create LLM client
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        base_url=os.getenv('OPENAI_BASE_URL')
    )
    model = "ElevenLabs"
    
    # Generate audio URL using LLM
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": document_content
            }
        ],
    )
    
    result = response.choices[0].message.content.strip()
    
    # Download MP3 file
    audio_response = requests.get(result)
    
    # Create output filename in audio_chapters folder
    source_path = Path(file_path)
    audio_dir = source_path.parent / "audio_chapters"
    audio_dir.mkdir(exist_ok=True)
    
    output_filename = source_path.stem + ".mp3"
    output_path = audio_dir / output_filename
    
    # Save MP3 file
    with open(output_path, 'wb') as f:
        f.write(audio_response.content)
    
    print(f"Audio saved to: {output_path}")
    return output_path

def process_chapters(chapters_dir="montesorri 12-15-months/chapters"):
    """Process all chapters and generate audio if content changed"""
    metadata = load_metadata()
    
    if not os.path.exists(chapters_dir):
        print(f"Chapters directory not found: {chapters_dir}")
        return
    
    # Find all markdown files
    chapter_files = sorted([f for f in os.listdir(chapters_dir) if f.endswith('.md')])
    
    for filename in chapter_files:
        file_path = os.path.join(chapters_dir, filename)
        chapter_name = filename.replace('.md', '')
        
        # Calculate current file hash
        current_hash = get_file_hash(file_path)
        
        # Check if we need to regenerate
        needs_generation = True
        if chapter_name in metadata:
            stored_hash = metadata[chapter_name].get('content_hash')
            audio_path = metadata[chapter_name].get('audio_path')
            
            # Skip if hash matches and audio file exists
            if stored_hash == current_hash and audio_path and os.path.exists(audio_path):
                print(f"Skipping {filename} - no changes detected")
                needs_generation = False
        
        if needs_generation:
            # Generate audio
            try:
                audio_path = generate_audio(file_path)
                duration = get_mp3_duration(audio_path)
                
                # Extract chapter title from markdown
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                title_match = content.split('\n')[0] if content else ""
                if title_match.startswith('# '):
                    chapter_title = title_match[2:].strip()
                else:
                    chapter_title = chapter_name.replace('-', ' ').title()
                
                # Update metadata
                metadata[chapter_name] = {
                    'content_hash': current_hash,
                    'audio_path': str(audio_path),
                    'duration_seconds': duration,
                    'source_file': file_path,
                    'generated_at': str(Path(audio_path).stat().st_mtime),
                    'title': chapter_title,
                    'word_count': len(content.split()) if content else 0,
                    'file_size_bytes': os.path.getsize(audio_path) if os.path.exists(audio_path) else 0
                }
                
                print(f"Generated audio for {filename} - Duration: {duration:.1f}s")
                
            except Exception as e:
                print(f"Error generating audio for {filename}: {e}")
                continue
    
    # Save updated metadata
    save_metadata(metadata)
    print(f"Metadata saved to {METADATA_FILE}")

def main():
    if len(sys.argv) > 1:
        # Single file mode
        file_path = sys.argv[1]
        generate_audio(file_path)
    else:
        # Process all chapters
        process_chapters()

if __name__ == '__main__':
    main()