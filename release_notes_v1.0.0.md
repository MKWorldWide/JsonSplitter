# JsonSplitter v1.0.0 Release Notes

## 🎉 Initial Release - JsonSplitter v1.0.0

A comprehensive toolkit for processing, organizing, and converting ChatGPT conversation JSON exports into multiple readable formats.

## ✨ Features

### 🔄 Multiple Splitting Modes
- **Monthly**: Split conversations by month (YYYY-MM)
- **Weekly**: Split by ISO week (YYYY-Www)
- **Title**: Individual conversations by title
- **Date-Title**: Hierarchical date folders with title files

### 📄 Flexible Output Formats
- **JSON**: Original format with various organization structures
- **Text**: Detailed format with timestamps and metadata
- **Book**: Clean, readable dialogue format
- **Master Book**: Single chronological file with chapters

### 🛠️ Advanced Features
- **Month Exclusion**: Skip specific months from processing
- **Batch Processing**: Handle entire directory structures
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Zero Dependencies**: Uses only Python standard library
- **Privacy-Focused**: Your data stays local

## 📦 Scripts Included

### Core Scripts
1. **split_conversations.py** - Main conversation splitter
2. **convert_conversations.py** - JSON to detailed text converter
3. **convert_to_book_format.py** - Text to book format converter
4. **create_master_book.py** - Master book creation tool

### Usage Examples
```bash
# Split conversations by title
python3 split_conversations.py conversations.json output --mode title

# Convert to readable format
python3 convert_conversations.py output output_text

# Create book format
python3 convert_to_book_format.py output_text output_book

# Create master book
python3 create_master_book.py output_book conversations_book.txt
```

## 🎯 Use Cases

- **Personal Archive**: Organize ChatGPT conversations systematically
- **Content Analysis**: Process conversations for research
- **Documentation**: Create readable records of discussions
- **Book Creation**: Turn conversations into a readable format
- **Backup**: Maintain organized conversation backups

## 📋 Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

## 🔧 Installation

```bash
git clone https://github.com/MKWorldWide/JsonSplitter.git
cd JsonSplitter
# No pip install required - uses built-in Python modules
```

## 📚 Documentation

- Complete README with installation and usage instructions
- Example commands for all features
- Technical specifications
- Contributing guidelines

## 🛡️ Privacy

- Your conversations.json file is excluded from Git
- All processing happens locally
- No data sent to external services

## 🌟 Highlights

- **1,298+ Conversations Processed**: Tested with large datasets
- **33MB Master Book**: Successfully created comprehensive book
- **Zero Dependencies**: Completely self-contained
- **Professional Documentation**: GitHub-ready project
- **Cross-Platform**: Works everywhere Python runs

## 🚀 Getting Started

1. Export your ChatGPT conversations as `conversations.json`
2. Run your desired splitting mode
3. Convert to your preferred format
4. Enjoy your organized conversations!

## 🙏 Acknowledgments

Built for ChatGPT users who want better conversation organization and management tools.

---

**Download and start organizing your conversations today! 🎉**
