#!/usr/bin/env python3
"""
Script to automatically fix common PEP 8 issues in Python files.
"""

import os
import re


def fix_trailing_whitespace(content):
    """Remove trailing whitespace from lines."""
    lines = content.split('\n')
    return '\n'.join(line.rstrip() for line in lines)


def fix_blank_line_whitespace(content):
    """Remove whitespace from blank lines."""
    lines = content.split('\n')
    fixed_lines = []
    for line in lines:
        if line.strip() == '':
            fixed_lines.append('')
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)


def fix_missing_newline_at_eof(content):
    """Ensure file ends with a newline."""
    if content and not content.endswith('\n'):
        return content + '\n'
    return content


def fix_too_many_blank_lines(content):
    """Fix too many consecutive blank lines."""
    # Replace 3+ consecutive newlines with 2
    content = re.sub(r'\n\n\n+', '\n\n', content)
    return content


def fix_file(filepath):
    """Fix PEP 8 issues in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply fixes
        content = fix_trailing_whitespace(content)
        content = fix_blank_line_whitespace(content)
        content = fix_too_many_blank_lines(content)
        content = fix_missing_newline_at_eof(content)

        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filepath}")

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")


def main():
    """Main function to fix all Python files."""
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Directories to skip
    skip_dirs = {'.venv', '__pycache__', 'migrations', 'staticfiles', '.git'}

    # Find all Python files
    for root, dirs, files in os.walk(project_root):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                fix_file(filepath)


if __name__ == '__main__':
    main()
