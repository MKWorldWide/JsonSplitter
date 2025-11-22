# Changelog

All notable changes to JsonSplitter will be documented in this file.

## [1.0.0] - 2024-11-21

### Added
- **split_conversations.py** - Main conversation splitter with multiple modes:
  - Month-based splitting (YYYY-MM)
  - Week-based splitting (YYYY-Www ISO weeks)
  - Title-based splitting (individual conversations)
  - Date-title hierarchical splitting (date folders with title files)
  - Month exclusion support (--out-months)
- **convert_conversations.py** - JSON to detailed text format converter
- **convert_to_book_format.py** - Text to book-readable format converter
- **create_master_book.py** - Master book creation from all conversations
- Comprehensive README with installation and usage instructions
- MIT License
- Complete documentation and examples
- Support for ChatGPT JSON export format
- Error handling and logging
- File sanitization for cross-platform compatibility

### Features
- **Multiple Output Formats**: JSON, detailed text, book format
- **Flexible Organization**: Monthly, weekly, by title, or hierarchical
- **Batch Processing**: Handle entire directory structures
- **Exclusion Support**: Skip specific months from processing
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Memory Efficient**: Processes files individually
- **Zero Dependencies**: Uses only Python standard library

### Output Examples
- Monthly: `conversations_2024-01.json`
- Weekly: `conversations_2024-W15.json`
- Title: `conversations_Specific_Topic.json`
- Hierarchical: `2024-01/conversations_Specific_Topic.json`
- Book format: Clean, readable dialogue style
- Master book: Single chronological file with chapters

### Documentation
- Complete README with installation guide
- Usage examples for all scripts
- Configuration options documentation
- Technical specifications
- Contributing guidelines
