#!/usr/bin/env python3
"""
GitHub Pages Publisher - Simple upload script
"""

import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class Publisher:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        
    def log(self, message, is_command=False):
        prefix = "[DRY RUN] " if self.dry_run else ""
        if is_command:
            prefix += "[CMD] "
        print(f"{prefix}{message}")
        
    def run_command(self, cmd):
        self.log(f"Running: {cmd}", is_command=True)
        
        if self.dry_run:
            return
            
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
        return result
            
    def find_files_to_publish(self):
        epub_files = list(Path('.').glob('*.epub'))
        audiobook_files = list(Path('.').glob('*.m4b'))
        
        if not epub_files and not audiobook_files:
            raise RuntimeError("No files to publish")
            
        return epub_files + audiobook_files
        
    def setup_gh_pages_branch(self):
        # Get current branch
        if not self.dry_run:
            result = self.run_command("git branch --show-current")
            original_branch = result.stdout.strip()
        else:
            original_branch = "main"  # dummy for dry run
        
        # Switch to gh-pages
        self.run_command("git checkout gh-pages")
        self.run_command("git pull origin gh-pages")
                
        return original_branch
        
    def publish(self):
        files_to_publish = self.find_files_to_publish()
        original_branch = self.setup_gh_pages_branch()
        
        try:
            # Copy files
            for file_path in files_to_publish:
                if not self.dry_run:
                    shutil.copy2(file_path, ".")
                self.log(f"Copied: {file_path.name}")
                
            # Copy download page
            if not self.dry_run:
                shutil.copy2("download-page.html", "index.html")
            self.log("Copied: download-page.html -> index.html")
            
            # Commit and push
            files_to_add = [f.name for f in files_to_publish] + ["index.html"]
                
            for file in files_to_add:
                self.run_command(f"git add {file}")
                
            commit_msg = f"Update files - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.run_command(f'git commit -m "{commit_msg}"')
            self.run_command("git push origin gh-pages")
            
            self.log("✅ Published successfully!")
            
        finally:
            if original_branch != "gh-pages":
                self.run_command(f"git checkout {original_branch}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', '-n', action='store_true')
    args = parser.parse_args()
    
    publisher = Publisher(dry_run=args.dry_run)
    publisher.publish()

if __name__ == '__main__':
    main()