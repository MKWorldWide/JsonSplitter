#!/usr/bin/env python3
"""
Split a big ChatGPT conversations.json export into smaller JSON files,
grouped by month or week.

Usage examples:

  # By month (default), outputs files like: conversations_2025-01.json
  python split_conversations.py conversations.json output_dir

  # By ISO week, outputs files like: conversations_2025-W03.json
  python split_conversations.py conversations.json output_dir --mode week

  # Exclude specific months from output
  python split_conversations.py conversations.json output_dir --out-months 2024-01 2024-02

  # Split by title into individual files
  python split_conversations.py conversations.json output_dir --mode title

  # Split by title with custom prefix
  python split_conversations.py conversations.json output_dir --mode title --prefix chat

  # Split by date then title (date folders containing title files)
  python split_conversations.py conversations.json output_dir --mode date_title
"""

import argparse
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Union

JsonType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]


def load_conversations(path: str) -> List[Dict[str, Any]]:
    """Load the conversations list from the JSON export."""
    with open(path, "r", encoding="utf-8") as f:
        data: JsonType = json.load(f)

    # Most exports are either:
    # 1) a list: [ {conversation1}, {conversation2}, ... ]
    # 2) an object with a key like "conversations": { ... }
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        # Try common key names
        for key in ("conversations", "items", "data"):
            if key in data and isinstance(data[key], list):
                return data[key]

    raise ValueError(
        "Could not find conversations list in JSON file. "
        "Root must be a list or contain a 'conversations' list."
    )


def get_timestamp(conv: Dict[str, Any]) -> float:
    """
    Extract a UNIX timestamp (seconds) from a conversation.

    We try create_time first, then update_time. If both missing/invalid,
    we return 0 so it falls into an 'unknown' bucket.
    """
    for key in ("create_time", "update_time"):
        value = conv.get(key)
        if isinstance(value, (int, float)):
            return float(value)
        # Sometimes timestamps are strings – try to parse them
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                pass
    return 0.0


def make_bucket_key(timestamp: float, mode: str, conversation: Dict[str, Any] = None) -> str:
    """
    Turn a timestamp or conversation into a bucket key:
      - mode == "month" -> "YYYY-MM"
      - mode == "week"  -> "YYYY-Www" (ISO week, e.g. 2025-W03)
      - mode == "title" -> sanitized title string
      - mode == "date_title" -> "YYYY-MM" for date grouping
    """
    if mode == "title":
        if conversation and "title" in conversation:
            title = conversation["title"]
            # Sanitize title for filename
            import re
            # Remove/replace invalid filename characters
            title = re.sub(r'[<>:"/\\|?*]', '_', title)
            title = re.sub(r'\s+', '_', title.strip())
            # Limit length for filesystem compatibility
            return title[:100] if len(title) > 100 else title
        return "untitled"
    
    if timestamp <= 0:
        return "unknown"

    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)

    if mode == "week":
        iso_year, iso_week, _ = dt.isocalendar()
        return f"{iso_year}-W{iso_week:02d}"
    elif mode == "date_title":
        return dt.strftime("%Y-%m")
    else:
        # default: month
        return dt.strftime("%Y-%m")


def group_conversations(
    conversations: List[Dict[str, Any]], mode: str
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group conversations into buckets by month, week, title, or date_title.
    Returns dict: {bucket_key: [conversation, ...], ...}
    """
    buckets: Dict[str, List[Dict[str, Any]]] = {}

    for conv in conversations:
        if mode == "title":
            key = make_bucket_key(0, mode, conv)
        else:
            ts = get_timestamp(conv)
            key = make_bucket_key(ts, mode)
        buckets.setdefault(key, []).append(conv)

    return buckets


def write_buckets(
    buckets: Dict[str, List[Dict[str, Any]]],
    output_dir: str,
    prefix: str = "conversations",
    out_months: List[str] = None,
    mode: str = "month",
) -> None:
    """Write each bucket as a separate JSON file in output_dir."""
    os.makedirs(output_dir, exist_ok=True)

    if mode == "date_title":
        # Special handling for date_title mode: create date directories with title files
        for date_bucket, convs in sorted(buckets.items()):
            # Skip if this date is in out_months
            if out_months and date_bucket in out_months:
                print(f"Skipping {date_bucket} ({len(convs)} conversations) - excluded month")
                continue
                
            # Create date directory
            date_dir = os.path.join(output_dir, date_bucket)
            os.makedirs(date_dir, exist_ok=True)
            
            # Group conversations by title within this date
            title_groups: Dict[str, List[Dict[str, Any]]] = {}
            for conv in convs:
                title_key = make_bucket_key(0, "title", conv)
                title_groups.setdefault(title_key, []).append(conv)
            
            # Write each title as a separate file in the date directory
            for title_key, title_convs in sorted(title_groups.items()):
                filename = f"{prefix}_{title_key}.json"
                out_path = os.path.join(date_dir, filename)
                
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(title_convs, f, ensure_ascii=False, indent=2)
                
                print(f"Wrote {len(title_convs):4d} conversations to {out_path}")
    else:
        # Standard handling for other modes
        for bucket_key, convs in sorted(buckets.items()):
            # Skip if this month is in out_months
            if out_months and bucket_key in out_months:
                print(f"Skipping {bucket_key} ({len(convs)} conversations) - excluded month")
                continue
                
            filename = f"{prefix}_{bucket_key}.json"
            out_path = os.path.join(output_dir, filename)

            # Write pretty JSON for readability; change indent=None to minify
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(convs, f, ensure_ascii=False, indent=2)

            print(f"Wrote {len(convs):4d} conversations to {out_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split a big ChatGPT conversations.json into smaller files "
                    "grouped by month or ISO week."
    )
    parser.add_argument("input", help="Path to conversations.json")
    parser.add_argument("output_dir", help="Directory to write split JSON files")
    parser.add_argument(
        "--mode",
        choices=["month", "week", "title", "date_title"],
        default="month",
        help="Group by 'month' (YYYY-MM), ISO 'week' (YYYY-Www), 'title', or 'date_title' (date folders with title files). Default: month.",
    )
    parser.add_argument(
        "--prefix",
        default="conversations",
        help="Filename prefix for output files. Default: 'conversations'",
    )
    parser.add_argument(
        "--out-months",
        nargs="*",
        help="Space-separated list of months to exclude (format: YYYY-MM). Example: --out-months 2024-01 2024-02",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print(f"Loading conversations from {args.input} ...")
    conversations = load_conversations(args.input)
    print(f"Loaded {len(conversations)} conversations.")

    print(f"Grouping by {args.mode} ...")
    buckets = group_conversations(conversations, args.mode)

    print(f"Writing {len(buckets)} bucket files into {args.output_dir} ...")
    write_buckets(buckets, args.output_dir, prefix=args.prefix, out_months=args.out_months, mode=args.mode)

    print("Done.")


if __name__ == "__main__":
    main()