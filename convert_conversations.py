#!/usr/bin/env python3
"""
Convert ChatGPT conversation JSON files to readable text format.

This script processes JSON conversation files and converts them to human-readable
text with timestamps, user prompts, assistant responses, and model information.

Usage:
  python convert_conversations.py input_json_file output_txt_file
  python convert_conversations.py input_directory output_directory
"""

import argparse
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
import re

def format_timestamp(timestamp: Optional[float]) -> str:
    """Convert Unix timestamp to readable format."""
    if timestamp is None or timestamp <= 0:
        return "[Unknown time]"
    
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")

def get_model_info(message: Dict[str, Any]) -> str:
    """Extract model information from message metadata."""
    metadata = message.get("metadata", {})
    model_info = []
    
    # Check for model slug in metadata
    if "model_slug" in metadata:
        model_info.append(f"Model: {metadata['model_slug']}")
    
    # Check for other model indicators
    if "message_type" in metadata and metadata["message_type"]:
        model_info.append(f"Type: {metadata['message_type']}")
    
    return " | ".join(model_info) if model_info else ""

def extract_content(message: Dict[str, Any]) -> str:
    """Extract text content from message."""
    content = message.get("content", {})
    if content.get("content_type") == "text":
        parts = content.get("parts", [])
        if parts and isinstance(parts, list):
            return "\n".join(str(part) for part in parts if part)
    return ""

def find_conversation_chain(mapping: Dict[str, Any], root_id: str) -> List[Dict[str, Any]]:
    """Build conversation chain from mapping structure."""
    messages = []
    
    def traverse(node_id: str):
        node = mapping.get(node_id)
        if not node:
            return
        
        message = node.get("message")
        if message and not message.get("metadata", {}).get("is_visually_hidden_from_conversation", False):
            # Skip empty system messages
            if not (message.get("author", {}).get("role") == "system" and not extract_content(message).strip()):
                messages.append(message)
        
        children = node.get("children", [])
        for child_id in children:
            traverse(child_id)
    
    traverse(root_id)
    return messages

def process_conversation(conversation: Dict[str, Any]) -> str:
    """Convert a single conversation to readable text."""
    title = conversation.get("title", "Untitled Conversation")
    create_time = conversation.get("create_time")
    update_time = conversation.get("update_time")
    mapping = conversation.get("mapping", {})
    
    # Find the root node (usually the first one with no parent)
    root_id = None
    for node_id, node in mapping.items():
        if node.get("parent") is None:
            root_id = node_id
            break
    
    if not root_id:
        return f"# {title}\n\n[No conversation data found]\n"
    
    # Build conversation chain
    messages = find_conversation_chain(mapping, root_id)
    
    # Format output
    output = []
    output.append(f"# {title}")
    output.append(f"Created: {format_timestamp(create_time)}")
    output.append(f"Updated: {format_timestamp(update_time)}")
    output.append("=" * 60)
    output.append("")
    
    current_exchange = []
    
    for i, message in enumerate(messages):
        author = message.get("author", {})
        role = author.get("role", "unknown")
        create_time = message.get("create_time")
        content = extract_content(message)
        model_info = get_model_info(message)
        
        if not content.strip():
            continue
        
        timestamp = format_timestamp(create_time)
        
        if role == "user":
            # Start new exchange
            if current_exchange:
                # Write previous exchange
                output.extend(current_exchange)
                output.append("")
                output.append("-" * 40)
                output.append("")
                current_exchange = []
            
            current_exchange.append(f"## User Prompt")
            current_exchange.append(f"**Time:** {timestamp}")
            current_exchange.append(f"**Content:** {content}")
            current_exchange.append("")
            
        elif role == "assistant":
            current_exchange.append(f"## Assistant Response")
            current_exchange.append(f"**Time:** {timestamp}")
            if model_info:
                current_exchange.append(f"**{model_info}**")
            current_exchange.append(f"**Content:** {content}")
            current_exchange.append("")
            
        elif role == "system":
            current_exchange.append(f"## System Message")
            current_exchange.append(f"**Time:** {timestamp}")
            current_exchange.append(f"**Content:** {content}")
            current_exchange.append("")
        
        elif role == "tool":
            current_exchange.append(f"## Tool Response")
            current_exchange.append(f"**Time:** {timestamp}")
            current_exchange.append(f"**Content:** {content}")
            current_exchange.append("")
    
    # Add final exchange
    if current_exchange:
        output.extend(current_exchange)
    
    return "\n".join(output)

def convert_file(input_path: str, output_path: str) -> None:
    """Convert a single JSON file to text."""
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if isinstance(data, list):
            # Handle multiple conversations
            all_text = []
            for conversation in data:
                text = process_conversation(conversation)
                all_text.append(text)
                all_text.append("\n" + "=" * 80 + "\n")
            
            result = "\n".join(all_text)
        else:
            # Handle single conversation
            result = process_conversation(data)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        
        print(f"Converted: {input_path} -> {output_path}")
        
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

def convert_directory(input_dir: str, output_dir: str) -> None:
    """Convert all JSON files in a directory."""
    if not os.path.exists(input_dir):
        print(f"Input directory does not exist: {input_dir}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all JSON files
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                input_path = os.path.join(root, file)
                
                # Create corresponding output path
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path.replace(".json", ".txt"))
                
                convert_file(input_path, output_path)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert ChatGPT conversation JSON files to readable text format."
    )
    parser.add_argument("input", help="Input JSON file or directory")
    parser.add_argument("output", help="Output text file or directory")
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
