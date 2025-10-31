#!/usr/bin/env python3

from playwright.sync_api import sync_playwright
from pathlib import Path
import os

def html_to_pdf_with_playwright():
    """Convert HTML to PDF using Playwright (Chrome)"""
    
    html_file = Path("comprehensive-accounting-integration-user-guide.html")
    pdf_file = Path("comprehensive-accounting-integration-user-guide.pdf")
    
    if not html_file.exists():
        print(f"Error: HTML file '{html_file}' not found!")
        return False
    
    # Get absolute path
    html_path = html_file.absolute()
    pdf_path = pdf_file.absolute()
    
    print(f"Converting {html_file.name} to PDF...")
    
    try:
        with sync_playwright() as p:
            # Launch browser in headless mode
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Load the HTML file
            page.goto(f"file://{html_path}")
            
            # Wait for content to load
            page.wait_for_load_state("networkidle")
            
            # Generate PDF with settings optimized for documentation
            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                margin={
                    "top": "20mm",
                    "right": "15mm", 
                    "bottom": "20mm",
                    "left": "15mm"
                },
                display_header_footer=True,
                header_template="""
                    <div style="font-size: 10px; text-align: center; width: 100%; margin: 0 50px;">
                        <span>Bayzat Accounting Integration - Comprehensive User Guide v2.0</span>
                    </div>
                """,
                footer_template="""
                    <div style="font-size: 10px; text-align: center; width: 100%; margin: 0 50px;">
                        <span class="pageNumber"></span> / <span class="totalPages"></span>
                    </div>
                """
            )
            
            browser.close()
            
            print(f"✅ PDF created successfully: {pdf_file}")
            
            # Check file size
            file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
            print(f"📄 File size: {file_size_mb:.2f} MB")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        print("\nPlease ensure Playwright is installed with browsers:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return False

if __name__ == "__main__":
    html_to_pdf_with_playwright()