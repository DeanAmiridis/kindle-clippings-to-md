# Kindle Clippings to Markdown

A lightweight Python script that converts Amazon Kindle `My Clippings.txt` exports into clean Markdown files.

The script:

- Parses Kindle highlights, notes, and bookmarks
- Groups entries by book
- Exports everything into a readable Markdown document
- Automatically timestamps output filenames
- Remembers previous input/output paths using a local `kindle.env` file

No external dependencies required.

---

# Features

- Interactive path prompts
- Persistent configuration using `kindle.env`
- Automatic dated Markdown exports
- UTF-8 safe parsing
- Supports large clipping files
- Cross-platform (macOS, Linux, Windows)

---

# Requirements

- Python 3.8 or newer

No pip packages are required.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/DeanAmiridis/kindle-clippings-to-md.git
cd kindle-clippings-to-md
```

Or simply download the script manually.

---

# Usage

Run the script:

```bash
python3 kindle-clippings-to-md.py
```

The script will prompt for:

1. Path to your `My Clippings.txt`
2. Output directory for the generated Markdown export

Example:

```text
Path to My Clippings.txt:
/Users/Dean/Documents/My Clippings.txt

Output folder path:
/Users/Dean/Documents/Kindle Exports
```

---

# Output Filename Format

Exports are automatically dated.

Example:

```text
05132026-My Clippings.md
```

Format:

```text
MMDDYYYY-My Clippings.md
```

---

# kindle.env Configuration File

The script automatically creates and updates a file named:

```text
kindle.env
```

This file stores the last-used paths so they do not need to be entered every time.

Example contents:

```env
CLIPPINGS_PATH="/Users/Dean/Documents/My Clippings.txt"
OUTPUT_PATH="/Users/Dean/Documents/Kindle Exports"
```

---

# Important

The script currently expects the environment filename to be exactly:

```text
kindle.env
```

This is controlled by the following line inside the script:

```python
ENV_FILE = Path(__file__).parent / "kindle.env"
```

If you rename the env file, you must also update this line.

---

# Example Markdown Output

```markdown
# Kindle My Clippings Export

## Atomic Habits — James Clear

*Highlight | location 123-126 | added Tuesday, May 13, 2026*

> Every action you take is a vote for the type of person you wish to become.

---
```

---

# Kindle Clippings File Location

Typical Kindle clippings file locations:

## Kindle Device

```text
documents/My Clippings.txt
```

## macOS

Usually copied manually from the Kindle device.

## Windows

Usually copied manually from the Kindle device.

---

# Notes

This script does not upload your highlights anywhere.

All parsing and conversion happens locally.

Unlike many web-based Kindle clipping tools, your data never leaves your machine.
