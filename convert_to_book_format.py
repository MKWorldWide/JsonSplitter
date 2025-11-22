#!/usr/bin/env python3
"""
Convert ChatGPT conversation text files to book-readable format.

This script processes the converted text files and reformats them to read
like a book with clean time stamps, prompts, and responses in flowing format.

Usage:
  python convert_to_book_format.py input_text_directory output_book_directory
"""

import argparse
import os
import re
from typing import List, Tuple

def parse_conversation_file(file_path: str) -> List[Tuple[str, str, str]]:
    """Parse a conversation text file and extract (time, role, content) tuples."""
    conversations = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    current_time = None
    current_role = None
    current_content = []
    
    for line in lines:
        line = line.rstrip("\n")
        
        # Detect time lines
        if line.startswith("**Time:** "):
            current_time = line.replace("**Time:** ", "")
            continue
        
        # Detect role headers
        if line.startswith("## "):
            if current_role and current_content:
                # Save previous conversation
                content = "\n".join(current_content).strip()
                if content:
                    conversations.append((current_time, current_role, content))
            
            current_role = line.replace("## ", "")
            current_content = []
            continue
        
        # Skip metadata lines and separators
        if (line.startswith("**") and "Content:" not in line) or \
           line.startswith("Created:") or \
           line.startswith("Updated:") or \
           line.startswith("=") or \
           line.startswith("-") or \
           line.startswith("# ") or \
           not line.strip():
            continue
        
        # Detect content start
        if line.startswith("**Content:** "):
            content = line.replace("**Content:** ", "")
            if content:
                current_content.append(content)
            continue
        
        # Add regular content lines
        if current_role and line.strip():
            current_content.append(line)
    
    # Save last conversation
    if current_role and current_content:
        content = "\n".join(current_content).strip()
        if content:
            conversations.append((current_time, current_role, content))
    
    return conversations

def format_as_book(conversations: List[Tuple[str, str, str]], title: str) -> str:
    """Format conversations as a readable book."""
    output = []
    
    # Add title
    output.append(f"{'='*60}")
    output.append(f"{title.upper()}")
    output.append(f"{'='*60}")
    output.append("")
    
    # Format each exchange
    for i, (time, role, content) in enumerate(conversations):
        if role == "User Prompt":
            # User message - format as question
            output.append(f"[{time}]")
            output.append(f"You: {content}")
            output.append("")
            
        elif role == "Assistant Response":
            # Assistant message - format as answer
            output.append(f"[{time}]")
            output.append(f"Assistant: {content}")
            output.append("")
            
            # Add separator between exchanges (except last one)
            if i < len(conversations) - 1:
                next_role = conversations[i + 1][1]
                if next_role == "User Prompt":
                    output.append("-" * 40)
                    output.append("")
    
    return "\n".join(output)

def convert_file(input_path: str, output_path: str) -> None:
    """Convert a single text file to book format."""
    try:
        # Extract title from filename
        filename = os.path.basename(input_path)
        title = filename.replace("conversations_", "").replace(".txt", "").replace("_", " ")
        
        # Parse conversations
        conversations = parse_conversation_file(input_path)
        
        if not conversations:
            print(f"No conversations found in {input_path}")
            return
        
        # Format as book
        book_content = format_as_book(conversations, title)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write book format
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(book_content)
        
        print(f"Converted: {input_path} -> {output_path}")
        
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

def convert_directory(input_dir: str, output_dir: str) -> None:
    """Convert all text files in a directory to book format."""
    if not os.path.exists(input_dir):
        print(f"Input directory does not exist: {input_dir}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all text files
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                input_path = os.path.join(root, file)
                
                # Create corresponding output path
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)
                
                convert_file(input_path, output_path)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert ChatGPT conversation text files to book-readable format."
    )
    parser.add_argument("input", help="Input text directory")
    parser.add_argument("output", help="Output book directory")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    
    if os.path.isfile(args.input):
        convert_file(args.input, args.output)
    elif os.path.isdir(args.input):
        convert_directory(args.input, args.output)
    else:
        print(f"Input path does not exist: {args.input}")

if __name__ == "__main__":
    main()
