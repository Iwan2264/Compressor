# FileCompressor App (Python + Flet)
===================================

A simple GUI application built with Flet that allows you to:
- Compress PDF files using Ghostscript with different quality presets.
- Compress images by adjusting quality with Pillow.
- General File & Folder Compression
    - Compress into .zip, .tar.gz, or .7z
    - Decompress .zip, .tar.gz, .7z, and .rar files

---

## Features

- PDF compression
- Image compression
- General file & folder compression and decompression
- Supports multiple formats: `.zip`, `.tar.gz`, `.7z`, `.rar` (read-only)
- Clean and modern UI built using Flet

---------------------
Requirements
---------------------

- **Python 3.8 or newer** (tested with 3.12.7)

- **[Ghostscript](https://ghostscript.com/)** - For PDF
  - **Windows:** Download from [Ghostscript for Windows](https://ghostscript.com/releases/gsdnld.html) and add `gswin64c` to your PATH.
  - **Linux/macOS:** Use your package manager, e.g.,  
    ```bash
    sudo apt-get install ghostscript  # Debian/Ubuntu
    brew install ghostscript           # macOS
    ```

- **Pillow** - For Image
  ```bash
  pip install Pillow


- **Flet** - Python GUI framework
  ```bash
  pip install flet

- **7-Zip CLI** (7z.exe) – Required for .7z and .rar support
  Download from https://www.7-zip.org/download.html
  Place 7z.exe in a bin/ folder relative to your project root or update the script path accordingly.

---------------------
How to Run the App
---------------------
Navigate to your project directory and run:
    ```bash
    python main.py

---------------------
Known Limitations
---------------------
- .rar compression is not supported (due to licensing restrictions)
- .rar decompression works if 7z.exe (7-Zip CLI) is available and inthe expected path.
- .gz format is not supported standalone — use .tar.gz instead

---------------------
License
---------------------
This project is open-source under the MIT License.
