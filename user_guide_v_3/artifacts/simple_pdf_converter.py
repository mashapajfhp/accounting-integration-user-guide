#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path

def convert_with_pandoc():
    """Convert HTML to PDF using pandoc if available"""
    
    html_file = "comprehensive-accounting-integration-user-guide.html"
    pdf_file = "comprehensive-accounting-integration-user-guide.pdf"
    
    print("Attempting to convert HTML to PDF using pandoc...")
    
    try:
        # Check if pandoc is installed
        result = subprocess.run(["which", "pandoc"], capture_output=True, text=True)
        if result.returncode != 0:
            print("pandoc not found. Installing via brew...")
            subprocess.run(["brew", "install", "pandoc"], check=True)
        
        # Convert using pandoc
        cmd = [
            "pandoc",
            html_file,
            "-o", pdf_file,
            "--pdf-engine=xelatex",
            "-V", "geometry:margin=1in",
            "-V", "documentclass=article",
            "-V", "fontsize=11pt",
            "-V", "linkcolor=blue",
            "-V", "urlcolor=blue"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PDF created successfully: {pdf_file}")
            file_size = os.path.getsize(pdf_file) / (1024 * 1024)
            print(f"📄 File size: {file_size:.2f} MB")
            return True
        else:
            print(f"pandoc failed: {result.stderr}")
            
    except Exception as e:
        print(f"Error with pandoc: {e}")
    
    return False

def create_simple_html_and_convert():
    """Create a simplified HTML version that converts better to PDF"""
    
    print("Creating simplified HTML for better PDF conversion...")
    
    # Read the original HTML
    with open("comprehensive-accounting-integration-user-guide.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create a simplified version with inline styles that work better for PDF
    simplified_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bayzat Accounting Integration - Comprehensive User Guide</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
            margin: 0;
            padding: 0;
            font-size: 11pt;
        }}
        
        h1 {{
            color: #6B46C1;
            border-bottom: 3px solid #6B46C1;
            padding-bottom: 10px;
            page-break-after: avoid;
            font-size: 24pt;
        }}
        
        h2 {{
            color: #374151;
            border-left: 4px solid #6B46C1;
            padding-left: 15px;
            page-break-after: avoid;
            margin-top: 20px;
            font-size: 18pt;
        }}
        
        h3 {{
            color: #4B5563;
            page-break-after: avoid;
            font-size: 14pt;
        }}
        
        h4 {{
            color: #6B7280;
            page-break-after: avoid;
            font-size: 12pt;
        }}
        
        .callout {{
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid;
            page-break-inside: avoid;
        }}
        
        .callout-critical {{
            background: #FEF2F2;
            border-color: #DC2626;
        }}
        
        .callout-warning {{
            background: #FEF3C7;
            border-color: #F59E0B;
        }}
        
        .callout-success {{
            background: #F0FDF4;
            border-color: #10B981;
        }}
        
        .callout-info {{
            background: #EFF6FF;
            border-color: #3B82F6;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            page-break-inside: avoid;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        
        th {{
            background-color: #f2f2f2;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            page-break-inside: avoid;
        }}
        
        pre {{
            background: #f4f4f4;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            page-break-inside: avoid;
        }}
        
        code {{
            background: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        
        .path-comparison {{
            display: table;
            width: 100%;
            page-break-inside: avoid;
        }}
        
        .path-card {{
            background: #f9f9f9;
            border: 1px solid #ddd;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            page-break-inside: avoid;
        }}
        
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        /* Force page breaks before major sections */
        #platform-limitations, #troubleshooting-kb, #health-checklist {{
            page-break-before: always;
        }}
        
        /* Prevent widows and orphans */
        p {{
            widows: 3;
            orphans: 3;
        }}
        
        /* Print-specific styles */
        @media print {{
            body {{
                font-size: 10pt;
            }}
            
            h1 {{
                font-size: 20pt;
            }}
            
            h2 {{
                font-size: 16pt;
            }}
            
            h3 {{
                font-size: 12pt;
            }}
            
            .no-print {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
"""
    
    # Extract body content from original HTML
    import re
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
        
        # Clean up some elements that don't convert well
        body_content = re.sub(r'<div class="search-container">.*?</div>', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'onclick="[^"]*"', '', body_content)
        body_content = re.sub(r'onkeyup="[^"]*"', '', body_content)
        
        simplified_html += body_content
    
    simplified_html += """
</body>
</html>
"""
    
    # Save simplified HTML
    simplified_file = "comprehensive-guide-simplified.html"
    with open(simplified_file, 'w', encoding='utf-8') as f:
        f.write(simplified_html)
    
    print(f"Created simplified HTML: {simplified_file}")
    print("\nYou can now:")
    print("1. Open the simplified HTML in Chrome/Safari")
    print("2. Press Cmd+P to print")
    print("3. Save as PDF with these settings:")
    print("   - Margins: Default")
    print("   - Print backgrounds: ON")
    print("   - Scale: 100%")
    
    return simplified_file

if __name__ == "__main__":
    # Try pandoc first
    if not convert_with_pandoc():
        # Fall back to creating simplified HTML
        simplified = create_simple_html_and_convert()
        print(f"\n✅ Created {simplified} for better PDF conversion")
        print("\nOpening in browser...")
        subprocess.run(["open", simplified])