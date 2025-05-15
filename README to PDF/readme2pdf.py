import argparse
import sys
import os
import markdown
from fpdf import FPDF, HTMLMixin

class MyFPDF(FPDF, HTMLMixin):
    pass

def convert_markdown_to_pdf_light(md_file_path, pdf_file_path, css_file_path=None):
    """
    Converts a Markdown file to PDF using markdown and fpdf2.
    Basic HTML styling from a CSS file can be attempted but is very limited.
    """
    if not os.path.exists(md_file_path):
        print(f"Error: Input Markdown file '{md_file_path}' not found.")
        sys.exit(1)

    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML
    # Enable extensions that fpdf2 might handle better, like tables
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # Basic CSS handling (very limited with fpdf2's HTMLMixin)
    style_string = ""
    if css_file_path:
        if os.path.exists(css_file_path):
            try:
                with open(css_file_path, 'r', encoding='utf-8') as f_css:
                    # fpdf2 doesn't directly parse CSS files for HTMLMixin in a comprehensive way.
                    # We can try to extract some very basic styles or use it as a reference.
                    # For now, we'll just note its presence.
                    # More advanced would be parsing CSS and applying styles programmatically via FPDF methods,
                    # which is beyond simple HTML rendering.
                    print(f"Info: CSS file '{css_file_path}' provided. "
                          "Note: fpdf2's HTML support has limited CSS handling.")
                    # Example: You could try to prepend some <style> tags if you know fpdf2 handles them.
                    # style_string = f"<style>{f_css.read()}</style>" # This may or may not work well
            except Exception as e:
                print(f"Warning: Could not read CSS file '{css_file_path}': {e}")
        else:
            print(f"Warning: CSS file '{css_file_path}' not found.")

    # Prepend style string if any (though its effect is limited)
    final_html = style_string + html_content

    pdf = MyFPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12) # Set a default font

    # Add a UTF-8 font if you expect non-Latin characters
    # Ensure you have a .ttf font file (e.g., DejaVuSans.ttf)
    try:
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)
    except RuntimeError:
        print("Warning: DejaVuSans.ttf not found. Using Arial. Non-ASCII characters might not render correctly.")
        print("You can download DejaVuSans.ttf and place it in the script's directory or specify a path.")

    pdf.write_html(final_html)
    pdf.output(pdf_file_path)

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to a PDF file (Lightweight Version).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "input_file",
        help="Path to the input Markdown file (.md)."
    )
    parser.add_argument(
        "-o", "--output_file",
        help="Path to the output PDF file. \nIf not specified, the output will be saved in the same directory \nas the input file with the same name but a .pdf extension."
    )
    parser.add_argument(
        "-c", "--css_file",
        help="Optional path to a custom CSS file for styling the PDF. \n(Note: CSS support is very limited with this lightweight version)."
    )

    args = parser.parse_args()

    input_md_file = args.input_file
    output_pdf_file = args.output_file
    css_path = args.css_file

    if not input_md_file.lower().endswith((".md", ".markdown")):
        print("Error: Input file must be a Markdown file (e.g., input.md)")
        sys.exit(1)

    if output_pdf_file is None:
        output_pdf_file = os.path.splitext(input_md_file)[0] + ".pdf"
    elif not output_pdf_file.lower().endswith(".pdf"):
        new_output_pdf_file = os.path.splitext(output_pdf_file)[0] + ".pdf"
        print(f"Warning: Output file name '{output_pdf_file}' did not end with .pdf. Saving as '{new_output_pdf_file}'.")
        output_pdf_file = new_output_pdf_file


    try:
        print(f"Converting '{input_md_file}' to '{output_pdf_file}'...")
        convert_markdown_to_pdf_light(input_md_file, output_pdf_file, css_path)
        print("Conversion successful!")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()