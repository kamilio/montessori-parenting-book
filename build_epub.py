#!/usr/bin/env python3
"""
EPUB Build Script for Montessori Parenting Content
Converts markdown chapters to EPUB format
"""

import os
import sys
import argparse
from pathlib import Path
from ebooklib import epub
import markdown


def read_markdown_file(file_path):
    """Read and convert markdown file to HTML"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Configure markdown with extensions that preserve formatting
    html = markdown.markdown(
        content, 
        extensions=[
            'extra',
            'nl2br',  # Converts newlines to <br> tags
            'sane_lists'  # Better list handling
        ]
    )
    return html


def create_epub_chapter(title, content, chapter_id, style):
    """Create an EPUB chapter from HTML content"""
    chapter = epub.EpubHtml(
        title=title,
        file_name=f'{chapter_id}.xhtml',
        lang='en'
    )
    
    # Wrap content with proper HTML and CSS
    html_content = f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <link rel="stylesheet" href="style/default.css" type="text/css"/>
</head>
<body>
{content}
</body>
</html>'''
    
    chapter.content = html_content
    return chapter


def create_css_style():
    """Create CSS style for EPUB"""
    css = '''
body {
    font-family: Georgia, serif;
    line-height: 1.6;
    margin: 2em;
    color: #333;
}

h1, h2, h3, h4, h5, h6 {
    color: #2c5530;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

p {
    margin-bottom: 1em;
    text-align: justify;
}

ul, ol {
    margin: 1em 0;
    padding-left: 2em;
    line-height: 1.8;
}

li {
    margin-bottom: 0.5em;
    display: list-item;
}

ul li {
    list-style-type: disc;
}

blockquote {
    margin: 1em 0;
    padding: 0.5em 1em;
    border-left: 4px solid #2c5530;
    background-color: #f9f9f9;
    font-style: italic;
}
'''
    
    style = epub.EpubItem(
        uid="style_default",
        file_name="style/default.css",
        media_type="text/css",
        content=css
    )
    
    return style


def build_epub(content_dir, output_path, title="Montessori Parenting Guide"):
    """Build EPUB from content directory"""
    print(f"Building EPUB: {title}")
    
    book = epub.EpubBook()
    book.set_identifier('montessori-parenting-guide')
    book.set_title(title)
    book.set_language('en')
    book.add_author('Montessori Parent')
    
    # Add CSS style
    style = create_css_style()
    book.add_item(style)
    
    # Add cover if exists
    cover_path = os.path.join(content_dir, 'book-cover.png')
    if os.path.exists(cover_path):
        with open(cover_path, 'rb') as f:
            book.set_cover("cover.png", f.read())
    
    chapters = []
    chapters_dir = os.path.join(content_dir, 'chapters')
    
    if os.path.exists(chapters_dir):
        chapter_files = sorted([f for f in os.listdir(chapters_dir) if f.endswith('.md')])
        
        for i, filename in enumerate(chapter_files):
            file_path = os.path.join(chapters_dir, filename)
            html_content = read_markdown_file(file_path)
            
            # Extract title from first H1 in content
            title_start = html_content.find('<h1>')
            title_end = html_content.find('</h1>')
            if title_start != -1 and title_end != -1:
                title_part = html_content[title_start+4:title_end]
            else:
                title_part = filename.replace('.md', '').replace('-', ' ').title()
            
            chapter_id = f'chapter_{i+1}'
            chapter = create_epub_chapter(title_part, html_content, chapter_id, style)
            book.add_item(chapter)
            chapters.append(chapter)
            
            print(f"Added chapter: {title_part}")
    
    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters
    
    epub.write_epub(output_path, book)
    print(f"EPUB created successfully: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Build EPUB from Montessori content')
    parser.add_argument('--content-dir', '-c', 
                       default='montesorri 12-15-months',
                       help='Directory containing content to convert')
    parser.add_argument('--output', '-o',
                       default='montessori-parenting-guide.epub',
                       help='Output EPUB filename')
    parser.add_argument('--title', '-t',
                       default='Montessori Parenting Guide (12-15 Months)',
                       help='Book title')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.content_dir):
        print(f"Error: Content directory '{args.content_dir}' not found")
        sys.exit(1)
    
    try:
        build_epub(args.content_dir, args.output, args.title)
        print(f"\nSuccess! EPUB file created: {args.output}")
    except Exception as e:
        print(f"Error building EPUB: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()