"""
Image Utilities Module
Handles downloading and processing images for the application.
"""
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os

# Cache directory for downloaded posters
CACHE_DIR = "assets/images/posters"

def ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def download_image(url, width=150, height=225):
    """
    Download an image from a URL and return it as a PhotoImage.
    
    Args:
        url: The URL of the image
        width: Target width for the image
        height: Target height for the image
    
    Returns:
        ImageTk.PhotoImage object, or None if download fails
    """
    try:
        # Reduced timeout for faster failures
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # Open image from bytes
        image = Image.open(BytesIO(response.content))
        
        # Resize image with faster algorithm for speed
        image = image.resize((width, height), Image.Resampling.BILINEAR)
        
        # Convert to PhotoImage for Tkinter
        return ImageTk.PhotoImage(image)
    
    except Exception as e:
        # Silent failure - just return None, don't print every error
        return None

def get_placeholder_image(width=150, height=225):
    """
    Create a placeholder image when poster is not available.
    
    Args:
        width: Image width
        height: Image height
    
    Returns:
        ImageTk.PhotoImage object
    """
    try:
        # Create a gray placeholder image with loading text
        from PIL import ImageDraw, ImageFont
        
        image = Image.new('RGB', (width, height), color='#333333')
        draw = ImageDraw.Draw(image)
        
        # Add loading text
        text = "Loading..."
        # Try to use a font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position (center)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Draw text
        draw.text(position, text, fill='#888888', font=font)
        
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error creating placeholder: {e}")
        # Fallback to simple gray box
        try:
            image = Image.new('RGB', (width, height), color='#333333')
            return ImageTk.PhotoImage(image)
        except:
            return None
