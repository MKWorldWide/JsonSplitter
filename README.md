# JsonSplitter - ChatGPT Conversation Processor

A comprehensive toolkit for processing, organizing, and converting ChatGPT conversation JSON exports into multiple readable formats.

## 🚀 Features

- **Multiple Splitting Modes**: Split conversations by month, week, title, or hierarchical date-title combinations
- **Flexible Output Formats**: JSON, readable text, and book-formatted files
- **Exclusion Support**: Skip specific months from processing
- **Batch Processing**: Handle entire directory structures automatically
- **Master Book Creation**: Combine all conversations into a single chronological book
- **Clean Organization**: Hierarchical directory structures for easy navigation

## 📁 Project Structure

```
JsonSplitter/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── split_conversations.py             # Main conversation splitter
├── convert_conversations.py           # JSON to text converter
├── convert_to_book_format.py          # Text to book format converter
├── create_master_book.py              # Master book creator
├── conversations.json                 # Your input file (add this)
├── output/                            # Monthly split files
├── output_by_title/                   # Individual conversations by title
├── output_by_date_title/              # Hierarchical date-title organization
├── output_with_exclusions/            # Monthly with excluded months
├── output_text/                       # Monthly conversations as text
├── output_by_title_text/              # Individual conversations as text
├── output_by_date_title_text/         # Hierarchical text format
├── output_by_date_title_book/         # Book-readable format
└── chatgpt_conversations_master_book.txt  # Complete master book
```

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/JsonSplitter.git
cd JsonSplitter
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Add your conversations file:**
   - Export your ChatGPT conversations as `conversations.json`
   - Place it in the project root directory

## 📖 Usage

### Basic Conversation Splitting

```bash
# Split by month (default)
python3 split_conversations.py conversations.json output

# Split by week
python3 split_conversations.py conversations.json output --mode week

# Split by individual conversation titles
python3 split_conversations.py conversations.json output_by_title --mode title

# Split hierarchically by date then title
python3 split_conversations.py conversations.json output_by_date_title --mode date_title
```

### Advanced Splitting with Exclusions

```bash
# Split by month but exclude specific months
python3 split_conversations.py conversations.json output_with_exclusions --out-months 2023-04 2023-05

# Hierarchical split with exclusions
python3 split_conversations.py conversations.json output_by_date_title_excluded --mode date_title --out-months 2023-04 2023-05
```

### Converting to Readable Formats

```bash
# Convert JSON files to detailed text format
python3 convert_conversations.py output output_text
python3 convert_conversations.py output_by_title output_by_title_text
python3 convert_conversations.py output_by_date_title output_by_date_title_text

# Convert to book-readable format
python3 convert_to_book_format.py output_by_date_title_text output_by_date_title_book
```

### Creating Master Book

```bash
# Combine all conversations into a single chronological book
python3 create_master_book.py output_by_date_title_book chatgpt_conversations_master_book.txt
```

## 📊 Output Formats

### 1. JSON Format
- **Monthly**: `conversations_2024-01.json` - All conversations from January 2024
- **Weekly**: `conversations_2024-W15.json` - All conversations from week 15 of 2024
- **Title**: `conversations_Specific_Topic.json` - Individual conversations by title
- **Date-Title**: `2024-01/conversations_Specific_Topic.json` - Hierarchical organization

### 2. Text Format
Detailed format with timestamps, roles, and metadata:
```
# Conversation Title
Created: 2024-01-15 10:30:00 UTC
Updated: 2024-01-15 10:45:00 UTC
============================================================

## User Prompt
**Time:** 2024-01-15 10:30:00 UTC
**Content:** Your question here...

## Assistant Response
**Time:** 2024-01-15 10:30:15 UTC
**Model:** gpt-4o
**Content:** Assistant's response here...
```

### 3. Book Format
Clean, readable format perfect for casual reading:
```
============================================================
CONVERSATION TITLE
============================================================

[2024-01-15 10:30:00 UTC]
You: Your question here...

[2024-01-15 10:30:15 UTC]
Assistant: Assistant's response here...

----------------------------------------
```

## ⚙️ Configuration Options

### split_conversations.py
- `--mode`: Choose splitting mode (`month`, `week`, `title`, `date_title`)
- `--prefix`: Custom filename prefix (default: "conversations")
- `--out-months`: Exclude specific months (format: YYYY-MM)

### convert_conversations.py
- Processes entire directory structures automatically
- Maintains original directory hierarchy
- Handles multiple conversations per file

### convert_to_book_format.py
- Creates clean, book-readable format
- Removes technical metadata
- Perfect for casual reading

### create_master_book.py
- Combines all conversations chronologically
- Creates monthly chapters
- Single file for easy reading

## 🎯 Use Cases

- **Personal Archive**: Organize your ChatGPT conversations systematically
- **Content Analysis**: Process conversations for research or analysis
- **Documentation**: Create readable records of important discussions
- **Book Creation**: Turn conversations into a readable book format
- **Backup**: Maintain organized backups of your conversation history

## 🔧 Technical Details

### Supported ChatGPT Export Format
The scripts work with the standard ChatGPT JSON export format containing:
- Conversation metadata (title, create_time, update_time)
- Message mapping structure with parent-child relationships
- Message content with roles (user, assistant, system, tool)
- Timestamp information

### File Naming Conventions
- **Invalid Characters**: Automatically replaced with underscores
- **Length Limits**: Titles truncated to 100 characters for filesystem compatibility
- **Date Formats**: ISO standard (YYYY-MM for months, YYYY-Www for weeks)

### Performance
- **Memory Efficient**: Processes files individually, suitable for large datasets
- **Batch Processing**: Handles entire directory structures automatically
- **Error Handling**: Graceful handling of malformed data with detailed logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add feature description'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📝 Examples

### Quick Start
```bash
# Process your conversations completely
python3 split_conversations.py conversations.json output_all --mode date_title
python3 convert_conversations.py output_all output_all_text
python3 convert_to_book_format.py output_all_text output_all_book
python3 create_master_book.py output_all_book my_conversations_book.txt
```

### Custom Organization
```bash
# Create monthly summaries excluding old conversations
python3 split_conversations.py conversations.json recent --out-months 2023-04 2023-05 2023-06
python3 convert_conversations.py recent recent_text
python3 convert_to_book_format.py recent_text recent_book
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Designed for ChatGPT users who want to organize their conversation history
- Inspired by the need for better conversation management tools
- Built with Python for cross-platform compatibility

## 📞 Support

If you encounter any issues or have questions:
1. Check the examples above
2. Ensure your `conversations.json` file is in the correct format
3. Verify Python dependencies are installed
4. Create an issue on GitHub with detailed information about your problem

---

**Happy organizing! 🎉**
