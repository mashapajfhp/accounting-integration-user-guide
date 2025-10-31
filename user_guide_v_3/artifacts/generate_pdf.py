#!/usr/bin/env python3

import os
from pathlib import Path

def convert_html_to_pdf():
    """
    Convert HTML file to PDF using wkhtmltopdf or weasyprint
    """
    html_file = Path("comprehensive-accounting-integration-user-guide.html")
    pdf_file = Path("comprehensive-accounting-integration-user-guide.pdf")
    
    if not html_file.exists():
        print(f"Error: HTML file '{html_file}' not found!")
        return False
    
    print(f"Converting {html_file} to PDF...")
    
    # First try with wkhtmltopdf (usually produces better results)
    try:
        import pdfkit
        
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'enable-local-file-access': None,
            'print-media-type': None,
            'no-outline': None
        }
        
        pdfkit.from_file(str(html_file), str(pdf_file), options=options)
        print(f"✅ PDF created successfully using pdfkit: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"pdfkit failed: {e}")
        print("Trying weasyprint...")
    
    # Try with weasyprint as fallback
    try:
        from weasyprint import HTML, CSS
        
        HTML(filename=str(html_file)).write_pdf(str(pdf_file))
        print(f"✅ PDF created successfully using weasyprint: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"weasyprint failed: {e}")
        print("Trying system command...")
    
    # Try direct system commands as last resort
    import subprocess
    
    # Try wkhtmltopdf command
    try:
        cmd = [
            "wkhtmltopdf",
            "--enable-local-file-access",
            "--print-media-type",
            "--page-size", "A4",
            "--margin-top", "19mm",
            "--margin-bottom", "19mm",
            "--margin-left", "19mm",
            "--margin-right", "19mm",
            str(html_file),
            str(pdf_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PDF created successfully using wkhtmltopdf command: {pdf_file}")
            return True
        else:
            print(f"wkhtmltopdf command failed: {result.stderr}")
    except Exception as e:
        print(f"wkhtmltopdf command not available: {e}")
    
    # Try weasyprint command
    try:
        cmd = ["weasyprint", str(html_file), str(pdf_file)]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PDF created successfully using weasyprint command: {pdf_file}")
            return True
        else:
            print(f"weasyprint command failed: {result.stderr}")
    except Exception as e:
        print(f"weasyprint command not available: {e}")
    
    print("\n❌ Failed to create PDF. Please install one of the following:")
    print("  1. pip install pdfkit && brew install wkhtmltopdf")
    print("  2. pip install weasyprint")
    print("\nOr use an online HTML to PDF converter.")
    return False

if __name__ == "__main__":
    convert_html_to_pdf()