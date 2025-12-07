"""
Generate WebP cover images from PDF first pages.
Requires: pip install pymupdf Pillow
"""

import fitz  # PyMuPDF
from PIL import Image
import io
import os

# Configuration
COMICS_DIR = "comics"
COVERS_DIR = "covers"
DPI = 150  # Resolution for rendering
QUALITY = 85  # WebP quality (0-100)

def generate_covers():
    # Create covers directory if it doesn't exist
    os.makedirs(COVERS_DIR, exist_ok=True)
    
    # Get all PDF files in comics directory
    pdf_files = [f for f in os.listdir(COMICS_DIR) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(COMICS_DIR, pdf_file)
        cover_name = os.path.splitext(pdf_file)[0] + ".webp"
        cover_path = os.path.join(COVERS_DIR, cover_name)
        
        print(f"Processing: {pdf_file}")
        
        try:
            # Open PDF and get first page
            doc = fitz.open(pdf_path)
            page = doc[0]
            
            # Render at high resolution
            zoom = DPI / 72  # 72 is default PDF DPI
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Save as WebP
            img.save(cover_path, 'WEBP', quality=QUALITY, method=6)
            
            doc.close()
            print(f"  ✓ Saved: {cover_path}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\nDone! Cover images saved to 'covers/' directory.")

if __name__ == "__main__":
    generate_covers()
