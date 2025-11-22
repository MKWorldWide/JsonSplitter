#!/usr/bin/env python3
"""
Create a master book file combining all conversations in chronological order.

This script combines all book-formatted conversations into a single
readable file organized by date and title.

Usage:
  python create_master_book.py input_book_directory output_master_book.txt
"""

import argparse
import os
from datetime import datetime

def parse_date_from_path(file_path: str) -> datetime:
    """Extract date from file path for sorting."""
    # Extract date from directory name (e.g., 2024-01)
    dir_name = os.path.basename(os.path.dirname(file_path))
    try:
        return datetime.strptime(dir_name, "%Y-%m")
    except ValueError:
        return datetime.min

def create_master_book(input_dir: str, output_path: str) -> None:
    """Create a master book combining all conversations."""
    if not os.path.exists(input_dir):
        print(f"Input directory does not exist: {input_dir}")
        return
    
    # Find all text files
    all_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                date = parse_date_from_path(file_path)
                all_files.append((date, file_path, file))
    
    # Sort by date, then by filename
    all_files.sort(key=lambda x: (x[0], x[2]))
    
    # Create master book
    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write("=" * 80 + "\n")
        out_f.write("CHATGPT CONVERSATIONS MASTER BOOK\n")
        out_f.write("=" * 80 + "\n\n")
        
        current_month = None
        conversation_count = 0
        
        for date, file_path, filename in all_files:
            # Add month header if changed
            month_str = date.strftime("%B %Y") if date != datetime.min else "Unknown Date"
            if month_str != current_month:
                current_month = month_str
                out_f.write("\n" + "=" * 60 + "\n")
                out_f.write(f"CHAPTER: {month_str.upper()}\n")
                out_f.write("=" * 60 + "\n\n")
            
            # Add conversation
            with open(file_path, "r", encoding="utf-8") as in_f:
                content = in_f.read()
                out_f.write(content)
                out_f.write("\n\n" + "=" * 80 + "\n\n")
            
            conversation_count += 1
            if conversation_count % 10 == 0:
                print(f"Processed {conversation_count} conversations...")
        
        # Add footer
        out_f.write("\n" + "=" * 80 + "\n")
        out_f.write(f"END OF BOOK - TOTAL CONVERSATIONS: {conversation_count}\n")
        out_f.write("=" * 80 + "\n")
    
    print(f"Master book created: {output_path}")
    print(f"Total conversations: {conversation_count}")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a master book combining all conversations."
    )
    parser.add_argument("input", help="Input book directory")
    parser.add_argument("output", help="Output master book file")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    create_master_book(args.input, args.output)

if __name__ == "__main__":
    main()
