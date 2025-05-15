# Lightweight Markdown to PDF Converter

A simple Python command-line tool to convert Markdown files to PDF format using the `markdown` and `fpdf2` libraries. This version prioritizes minimal dependencies.

## Features

* Convert local Markdown files to PDF.
* Specify an output file name and path.
* Basic support for Markdown features like headings, lists, bold, italics, and simple tables.
* Lightweight: Relies on pure Python libraries that are easy to install via pip.

## Limitations

* **Styling (CSS):** The `fpdf2` library has very basic HTML rendering capabilities. It does **not** support external CSS files in a comprehensive way, nor does it handle complex HTML/CSS layouts. The primary goal is content conversion, not precise visual replication of styled HTML.
* **Complex HTML/Markdown:** Advanced Markdown syntax that renders into complex HTML structures or relies heavily on CSS for its appearance might not be rendered accurately or styled as expected.
* **Font Support:** For broad character support (e.g., non-Latin characters), you might need to ensure a suitable UTF-8 font (like DejaVuSans.ttf) is available to the script. The script attempts to use DejaVuSans if present.

## Prerequisites

* Python 3.6+
* `pip` (Python package installer)

## Installation

1.  **Clone the repository (or download the script):**
    ```bash
    # If you have this in a git repository
    # git clone <your-repo-url>
    # cd <your-repo-name>
    ```
    Alternatively, just save the `md_to_pdf_light.py` script to your local machine.

2.  **Install dependencies:**
    ```bash
    pip install markdown fpdf2
    ```

3.  **(Optional) For better character support:**
    Download a Unicode TTF font like [DejaVu Sans](https://dejavu-fonts.github.io/). Place the `DejaVuSans.ttf` file in the same directory as the script, or provide a path to it if you modify the script.

## Usage

Run the script from your terminal:

```bash
python md_to_pdf_light.py <input_file.md> [options]