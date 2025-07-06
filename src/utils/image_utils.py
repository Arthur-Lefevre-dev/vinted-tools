"""
Image utilities for PDF Combiner application
"""

import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Optional, Tuple
from ..config import config
from ..exceptions import ImageProcessingError


def create_blank_image(width: int, height: int) -> Image.Image:
    """Create a blank white image with specified dimensions"""
    try:
        return Image.new('RGB', (width, height), 'white')
    except Exception as e:
        raise ImageProcessingError(f"Failed to create blank image: {str(e)}")


def resize_image_for_preview(image: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
    """Resize image to fit within max_size while maintaining aspect ratio"""
    try:
        # Calculate aspect ratio
        aspect_ratio = image.width / image.height
        max_width, max_height = max_size
        
        # Calculate new dimensions
        if aspect_ratio > 1:  # Landscape
            new_width = min(max_width, image.width)
            new_height = int(new_width / aspect_ratio)
        else:  # Portrait
            new_height = min(max_height, image.height)
            new_width = int(new_height * aspect_ratio)
        
        # Ensure minimum dimensions
        new_width = max(1, new_width)
        new_height = max(1, new_height)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    except Exception as e:
        raise ImageProcessingError(f"Failed to resize image: {str(e)}")


def convert_pil_to_ctk_image(pil_image: Image.Image) -> ctk.CTkImage:
    """Convert PIL Image to CustomTkinter image"""
    try:
        return ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=pil_image.size)
    except Exception as e:
        raise ImageProcessingError(f"Failed to convert image: {str(e)}")


def apply_orientation_transform(image: Image.Image, orientation: str) -> Image.Image:
    """Apply orientation transformation to image"""
    try:
        if orientation == "Paysage":
            return image.rotate(90, expand=True)
        return image  # Portrait - no rotation needed
    except Exception as e:
        raise ImageProcessingError(f"Failed to apply orientation: {str(e)}")


def crop_image_half(image: Image.Image, top_half: bool = True) -> Image.Image:
    """Crop image to get top or bottom half"""
    try:
        width, height = image.size
        if top_half:
            return image.crop((0, 0, width, height // 2))
        else:
            return image.crop((0, height // 2, width, height))
    except Exception as e:
        raise ImageProcessingError(f"Failed to crop image: {str(e)}")


def combine_images_vertically(top_image: Image.Image, bottom_image: Image.Image) -> Image.Image:
    """Combine two images vertically"""
    try:
        # Get dimensions
        top_width, top_height = top_image.size
        bottom_width, bottom_height = bottom_image.size
        
        # Calculate target width (maximum of both)
        target_width = max(top_width, bottom_width)
        
        # Resize images if needed
        if top_width != target_width:
            top_image = top_image.resize((target_width, top_height), Image.Resampling.LANCZOS)
        if bottom_width != target_width:
            bottom_image = bottom_image.resize((target_width, bottom_height), Image.Resampling.LANCZOS)
        
        # Create combined image
        combined_height = top_height + bottom_height
        combined_image = Image.new('RGB', (target_width, combined_height), 'white')
        
        # Paste images
        combined_image.paste(top_image, (0, 0))
        combined_image.paste(bottom_image, (0, top_height))
        
        return combined_image
    except Exception as e:
        raise ImageProcessingError(f"Failed to combine images: {str(e)}")


def save_image_with_format(image: Image.Image, file_path: str, format_type: str, 
                          quality: int = 100, dpi: int = 300) -> None:
    """Save image with specified format and quality"""
    try:
        if format_type.upper() == "PDF":
            image.save(file_path, 'PDF', quality=quality, resolution=float(dpi))
        elif format_type.upper() == "PNG":
            image.save(file_path, 'PNG', quality=quality, dpi=(dpi, dpi))
        else:
            raise ImageProcessingError(f"Unsupported format: {format_type}")
    except Exception as e:
        raise ImageProcessingError(f"Failed to save image: {str(e)}")


def get_image_info(image: Image.Image) -> dict:
    """Get image information"""
    return {
        'width': image.width,
        'height': image.height,
        'mode': image.mode,
        'format': image.format or 'Unknown',
        'size_mb': len(image.tobytes()) / (1024 * 1024)
    } 