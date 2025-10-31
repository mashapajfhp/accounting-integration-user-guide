#!/usr/bin/env python3
"""
Reliable PDF Generation Script for Bayzat Accounting Integration Guide
This script uses Playwright as the primary method, with fallbacks for reliability.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

def generate_pdf_with_playwright(html_file, pdf_file):
    """
    Generate PDF using Playwright (most reliable method).
    This produces high-quality PDFs similar to Chrome's print-to-PDF.
    """
    try:
        from playwright.sync_api import sync_playwright
        
        html_path = Path(html_file).absolute()
        pdf_path = Path(pdf_file).absolute()
        
        if not html_path.exists():
            raise FileNotFoundError(f"HTML file not found: {html_path}")
        
        print(f"🚀 Generating PDF with Playwright...")
        print(f"   Source: {html_path.name}")
        print(f"   Output: {pdf_path.name}")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            
            # Create new page with specific viewport
            page = browser.new_page(
                viewport={"width": 1280, "height": 800},
                device_scale_factor=2  # Higher quality rendering
            )
            
            # Navigate to the HTML file
            file_url = f"file://{html_path}"
            page.goto(file_url, wait_until="networkidle")
            
            # Wait a bit more for any dynamic content
            page.wait_for_timeout(2000)
            
            # Generate PDF with optimal settings
            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,  # Include background colors and images
                scale=0.95,  # Slightly scale down to avoid cutoff
                margin={
                    "top": "15mm",
                    "right": "10mm",
                    "bottom": "15mm",
                    "left": "10mm"
                },
                display_header_footer=True,
                header_template="""
                    <div style="width: 100%; font-size: 9px; padding: 5px 50px; text-align: center; color: #666;">
                        <span style="font-weight: bold;">Bayzat Accounting Integration Guide</span> - Comprehensive Edition v2.0
                    </div>
                """,
                footer_template="""
                    <div style="width: 100%; font-size: 9px; padding: 5px 50px; display: flex; justify-content: space-between; color: #666;">
                        <div style="text-align: left;">Generated: """ + datetime.now().strftime("%B %d, %Y") + """</div>
                        <div style="text-align: center;">
                            Page <span class="pageNumber"></span> of <span class="totalPages"></span>
                        </div>
                        <div style="text-align: right;">© Bayzat</div>
                    </div>
                """,
                prefer_css_page_size=True,
                outline=True  # Generate PDF outline from headings
            )
            
            # Get file size for reporting
            file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
            
            # Take a screenshot of first page for reference (optional)
            screenshot_path = pdf_path.parent / f"{pdf_path.stem}_preview.png"
            page.screenshot(path=str(screenshot_path), full_page=False)
            
            browser.close()
            
            print(f"✅ PDF generated successfully!")
            print(f"   📄 File size: {file_size_mb:.2f} MB")
            print(f"   📸 Preview saved: {screenshot_path.name}")
            
            return True
            
    except ImportError:
        print("❌ Playwright not installed. Run: pip3 install playwright && python3 -m playwright install chromium")
        return False
    except Exception as e:
        print(f"❌ Playwright PDF generation failed: {e}")
        return False

def generate_pdf_with_weasyprint(html_file, pdf_file):
    """
    Fallback method using WeasyPrint.
    Note: May require additional system dependencies.
    """
    try:
        from weasyprint import HTML, CSS
        
        print(f"🔄 Trying WeasyPrint as fallback...")
        
        HTML(filename=html_file).write_pdf(
            pdf_file,
            stylesheets=[CSS(string='''
                @page {
                    size: A4;
                    margin: 15mm;
                    @bottom-center {
                        content: counter(page) " / " counter(pages);
                    }
                }
            ''')]
        )
        
        file_size_mb = os.path.getsize(pdf_file) / (1024 * 1024)
        print(f"✅ PDF generated with WeasyPrint!")
        print(f"   📄 File size: {file_size_mb:.2f} MB")
        return True
        
    except Exception as e:
        print(f"❌ WeasyPrint failed: {e}")
        return False

def main():
    """Main function to generate PDF with automatic fallback."""
    
    # Configuration
    HTML_FILE = "comprehensive-accounting-integration-user-guide.html"
    PDF_FILE = "comprehensive-accounting-integration-user-guide.pdf"
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("🔧 Bayzat Accounting Integration Guide - PDF Generator")
    print("=" * 60)
    
    # Check if HTML file exists
    if not Path(HTML_FILE).exists():
        print(f"❌ Error: HTML file '{HTML_FILE}' not found!")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Available HTML files:")
        for f in Path(".").glob("*.html"):
            print(f"     - {f.name}")
        return 1
    
    # Backup existing PDF if it exists
    if Path(PDF_FILE).exists():
        backup_name = f"{Path(PDF_FILE).stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        os.rename(PDF_FILE, backup_name)
        print(f"📦 Backed up existing PDF to: {backup_name}")
    
    # Try Playwright first (best quality)
    success = generate_pdf_with_playwright(HTML_FILE, PDF_FILE)
    
    # Fallback to WeasyPrint if Playwright fails
    if not success:
        success = generate_pdf_with_weasyprint(HTML_FILE, PDF_FILE)
    
    # Final status
    if success:
        print("\n" + "=" * 60)
        print("🎉 PDF generation complete!")
        print(f"📄 Output: {PDF_FILE}")
        print("\n💡 Tip: For future use, just run:")
        print(f"   python3 {Path(__file__).name}")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ PDF generation failed!")
        print("\n📝 To fix this, install dependencies:")
        print("   pip3 install playwright")
        print("   python3 -m playwright install chromium")
        print("\nOr as fallback:")
        print("   pip3 install weasyprint")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())