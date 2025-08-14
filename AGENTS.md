Write only markdown 
- easy to read format, engaging

# Memory
Document any style input in the style.md file. When user gives instructions e.g. shorter, document that first before rewriting, but keep is super brief like 1 line max.

# Guidelines
No table of contents
When rewriting, make changes paragraph by paragraph and put a lot of effort into it.
Do not create new file for rewrites, edit existing
Use the `python analyze_chapters.py` to verify lengths

# Characters
Use only `characters.md`

# Commits - when asked
One-line commit messages
Small commits
Aim to commit all files even unrelated to current task

# Tools - cli scripts
No exception handling
No readme
No command line arguments unless requested
No fallbacks

## Available tools

### Length analyzer
Keep below 9000 tokens per chapter, check after each rewrite
`python analyze_chapters.py`

### Audio conversion
`python /Users/kjopek/Workspace/todos/projects/hiring/text2voice.py <file>`