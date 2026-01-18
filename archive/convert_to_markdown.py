#!/usr/bin/env python3
"""
Convert Word (.docx) files to Markdown format
"""
import os
from pathlib import Path
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table

def paragraph_to_markdown(paragraph):
    """Convert a Word paragraph to markdown format"""
    text = paragraph.text.strip()

    if not text:
        return ""

    # Check paragraph style for headings
    try:
        style_name = paragraph.style.name.lower() if paragraph.style and paragraph.style.name else ""
    except:
        style_name = ""

    if 'heading 1' in style_name:
        return f"# {text}\n"
    elif 'heading 2' in style_name:
        return f"## {text}\n"
    elif 'heading 3' in style_name:
        return f"### {text}\n"
    elif 'heading 4' in style_name:
        return f"#### {text}\n"
    elif 'heading 5' in style_name:
        return f"##### {text}\n"
    elif 'heading 6' in style_name:
        return f"###### {text}\n"
    elif 'list bullet' in style_name or 'list' in style_name:
        return f"- {text}\n"
    else:
        return f"{text}\n"

def table_to_markdown(table):
    """Convert a Word table to markdown format"""
    if not table.rows:
        return ""

    markdown_lines = []

    # Process header row
    header_cells = [cell.text.strip() for cell in table.rows[0].cells]
    markdown_lines.append("| " + " | ".join(header_cells) + " |")
    markdown_lines.append("| " + " | ".join(["---"] * len(header_cells)) + " |")

    # Process data rows
    for row in table.rows[1:]:
        cells = [cell.text.strip() for cell in row.cells]
        markdown_lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(markdown_lines) + "\n"

def convert_docx_to_markdown(docx_path):
    """Convert a .docx file to markdown"""
    doc = Document(docx_path)
    markdown_content = []

    for element in doc.element.body:
        if element.tag.endswith('p'):
            # It's a paragraph
            paragraph = Paragraph(element, doc)
            md_text = paragraph_to_markdown(paragraph)
            if md_text:
                markdown_content.append(md_text)
        elif element.tag.endswith('tbl'):
            # It's a table
            table = Table(element, doc)
            md_table = table_to_markdown(table)
            if md_table:
                markdown_content.append(md_table)

    return "\n".join(markdown_content)

def main():
    base_path = Path("/Users/lukepeterson/Desktop/Git Projects/WHYGOs")

    # Find all .docx files
    docx_files = list(base_path.rglob("*.docx"))

    # Filter out temporary files (starting with ~$)
    docx_files = [f for f in docx_files if not f.name.startswith("~$")]

    print(f"Found {len(docx_files)} Word files to convert\n")

    for docx_file in docx_files:
        try:
            print(f"Converting: {docx_file.name}")

            # Convert to markdown
            markdown_content = convert_docx_to_markdown(docx_file)

            # Create output path (same location, .md extension)
            md_file = docx_file.with_suffix('.md')

            # Write markdown file
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            print(f"  ✓ Created: {md_file.name}\n")

        except Exception as e:
            print(f"  ✗ Error converting {docx_file.name}: {e}\n")

    print("Conversion complete!")

if __name__ == "__main__":
    main()
