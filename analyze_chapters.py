#!/usr/bin/env python3

import os
import re
from pathlib import Path
from typing import Dict, List, Union
import tiktoken


def count_words(text: str) -> int:
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*{1,2}([^\*]+)\*{1,2}', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'^[\s]*[-\*\d]+\.?\s+', '', text, flags=re.MULTILINE)
    words = text.split()
    return len(words)


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count tokens using tiktoken encoding."""
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    return len(tokens)


def estimate_tts_duration(word_count: int, wpm: int = 150) -> Dict[str, Union[float, str]]:
    minutes = word_count / wpm
    hours = minutes / 60
    
    if hours >= 1:
        hours_int = int(hours)
        minutes_remainder = int((hours - hours_int) * 60)
        duration_str = f"{hours_int}h {minutes_remainder}m"
    else:
        duration_str = f"{int(minutes)}m {int((minutes - int(minutes)) * 60)}s"
    
    return {
        'minutes': round(minutes, 2),
        'hours': round(hours, 2),
        'formatted': duration_str
    }


def analyze_file(filepath: Path) -> Dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    word_count = count_words(content)
    char_count = len(content)
    token_count = count_tokens(content)
    
    tts_slow = estimate_tts_duration(word_count, wpm=130)
    tts_normal = estimate_tts_duration(word_count, wpm=150)
    tts_fast = estimate_tts_duration(word_count, wpm=170)
    
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else filepath.stem
    
    return {
        'file': filepath.name,
        'path': str(filepath),
        'title': title,
        'statistics': {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'words': word_count,
            'characters': char_count,
            'tokens': token_count,
            'avg_words_per_line': round(word_count / len(non_empty_lines), 1) if non_empty_lines else 0
        },
        'tts_duration': {
            'slow_130wpm': tts_slow,
            'normal_150wpm': tts_normal,
            'fast_170wpm': tts_fast
        }
    }


def find_markdown_files(directory: Path) -> List[Path]:
    return sorted(directory.rglob('*.md'))


def print_analysis(analysis: Dict, verbose: bool = True):
    print(f"\n📖 {analysis['title']}")
    print(f"   File: {analysis['path']}")
    
    stats = analysis['statistics']
    print(f"   📊 Statistics:")
    print(f"      • Words: {stats['words']:,}")
    print(f"      • Tokens: {stats['tokens']:,}")
    print(f"      • Lines: {stats['non_empty_lines']:,} (non-empty) / {stats['total_lines']:,} (total)")
    print(f"      • Characters: {stats['characters']:,}")
    print(f"      • Avg words/line: {stats['avg_words_per_line']}")
    
    tts = analysis['tts_duration']['normal_150wpm']
    print(f"   🎙️ TTS Duration (150 wpm): {tts['formatted']} ({tts['minutes']} minutes)")
    
    if verbose:
        print(f"      • Slow (130 wpm): {analysis['tts_duration']['slow_130wpm']['formatted']}")
        print(f"      • Fast (170 wpm): {analysis['tts_duration']['fast_170wpm']['formatted']}")


def main():
    base_dir = Path('montesorri 12-15-months')
    
    print(f"🔍 Analyzing chapters in '{base_dir}'...\n")
    print("=" * 70)
    
    markdown_files = find_markdown_files(base_dir)
    
    total_words = 0
    total_tokens = 0
    total_lines = 0
    file_count = 0
    
    for filepath in markdown_files:
        analysis = analyze_file(filepath)
        
        total_words += analysis['statistics']['words']
        total_tokens += analysis['statistics']['tokens']
        total_lines += analysis['statistics']['non_empty_lines']
        file_count += 1
        
        print_analysis(analysis, verbose=False)
    
    print("\n" + "=" * 70)
    print("\n📚 SUMMARY")
    print(f"   Total files: {file_count}")
    print(f"   Total words: {total_words:,}")
    print(f"   Total tokens: {total_tokens:,}")
    print(f"   Total lines: {total_lines:,}")
    
    total_tts = estimate_tts_duration(total_words)
    print(f"\n   🎙️ Total TTS Duration (150 wpm): {total_tts['formatted']}")
    print(f"      • Slow (130 wpm): {estimate_tts_duration(total_words, 130)['formatted']}")
    print(f"      • Fast (170 wpm): {estimate_tts_duration(total_words, 170)['formatted']}")


if __name__ == '__main__':
    main()