.PHONY: install build-epub generate-audio-chapters generate-audiobook publish clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  make install               - Install Python dependencies"
	@echo "  make build-epub            - Build EPUB from markdown chapters"
	@echo "  make generate-audio-chapters - Generate MP3 audio for all chapters"
	@echo "  make generate-audiobook    - Create M4B audiobook from MP3 files"
	@echo "  make publish               - Publish EPUB and audiobook to GitHub Pages"
	@echo "  make clean                 - Remove generated files"

# Install dependencies
install:
	pip3 install -r requirements.txt
	@echo "Installing m4b-tool dependencies..."
	@command -v brew >/dev/null 2>&1 && brew install ffmpeg php composer || echo "Please install ffmpeg, php, and composer manually"
	@command -v composer >/dev/null 2>&1 && composer global require sandreas/m4b-tool || echo "Please install composer first"
	@echo "Installation complete!"

# Build EPUB
build-epub:
	python3 build_epub.py
	@echo "EPUB built successfully!"

# Generate audio chapters
generate-audio-chapters:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Copy .env.example to .env and add your OpenAI API key"; \
		exit 1; \
	fi
	python3 generate_audio.py
	@echo "Audio chapters generated successfully!"

# Generate audiobook (M4B)
generate-audiobook: generate-audio-chapters
	python3 create_audiobook.py
	@echo "Audiobook (M4B) created successfully!"

# Publish to GitHub Pages
publish: build-epub generate-audiobook
	python3 publish.py
	@echo "Published to GitHub Pages successfully!"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f "montesorri 12-15-months/Montessori Toddler Guide.epub"
	@rm -f "montesorri 12-15-months/Montessori Toddler Guide.m4b"
	@echo "Clean complete!"