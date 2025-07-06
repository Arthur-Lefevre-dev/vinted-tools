"""
PDF processing core functionality
"""

import os
from typing import Optional, Tuple
from PIL import Image
from pdf2image import convert_from_path

from ..models import PDFDocument, CombinedDocument, ExportConfig, Orientation
from ..config import config
from ..exceptions import PDFLoadError, ValidationError, ImageProcessingError
from ..utils import (
    validate_pdf_file,
    create_blank_image,
    apply_orientation_transform,
    crop_image_half,
    combine_images_vertically,
    save_image_with_format,
    resize_image_for_preview
)


class PDFProcessor:
    """Core PDF processing functionality"""
    
    def __init__(self):
        self.pdf1 = PDFDocument()
        self.pdf2 = PDFDocument()
        self.combined = CombinedDocument()
        
        # Configure environment to avoid cmd windows
        self._configure_pdf2image_environment()
    
    def _get_poppler_path(self) -> Optional[str]:
        """Get poppler path for pdf2image"""
        import sys
        
        # When compiled, poppler is included in the executable
        if getattr(sys, 'frozen', False):
            # For compiled executable, return None to use system poppler
            return None
        else:
            # For development, return None to use system poppler
            return None
    
    def _configure_pdf2image_environment(self):
        """Configure environment to avoid cmd windows"""
        import subprocess
        import sys
        import os
        
        # Set environment variables to avoid cmd windows
        if sys.platform == 'win32':
            # Hide console windows on Windows
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # Set environment variables
            os.environ['PYTHONHASHSEED'] = '0'
    
    def _convert_pdf_safe(self, file_path: str, dpi: int, first_page: int = 1, last_page: int = 1):
        """Safely convert PDF to images without cmd windows"""
        import subprocess
        import sys
        
        # Configure subprocess to avoid cmd windows
        kwargs = {
            'first_page': first_page,
            'last_page': last_page,
            'dpi': dpi,
            'poppler_path': self._get_poppler_path(),
            'use_pdftocairo': True,
            'thread_count': 1
        }
        
        # Add Windows-specific settings to avoid cmd windows
        if sys.platform == 'win32':
            # Create a custom environment
            import os
            env = os.environ.copy()
            
            # Set console creation flags
            kwargs['fmt'] = 'ppm'  # Use PPM format for better compatibility
        
        return convert_from_path(file_path, **kwargs)
    
    def load_pdf_from_file(self, file_path: str, pdf_number: int) -> None:
        """Load PDF from file path"""
        if not validate_pdf_file(file_path):
            raise PDFLoadError(f"Invalid PDF file: {file_path}")
        
        try:
            # Load preview (low resolution)
            preview_images = self._convert_pdf_safe(
                file_path, 
                dpi=config.PREVIEW_DPI,
                first_page=1, 
                last_page=1
            )
            
            if not preview_images:
                raise PDFLoadError("No pages found in PDF")
            
            # Store the document
            pdf_doc = self.pdf1 if pdf_number == 1 else self.pdf2
            pdf_doc.file_path = file_path
            pdf_doc.is_blank = False
            pdf_doc.preview_image = preview_images[0]
            pdf_doc.hires_image = None  # Will be loaded when needed
            
        except Exception as e:
            raise PDFLoadError(f"Failed to load PDF: {str(e)}")
    
    def load_blank_page(self, pdf_number: int) -> None:
        """Load blank page"""
        try:
            blank_image = create_blank_image(
                config.A4_WIDTH_300DPI, 
                config.A4_HEIGHT_300DPI
            )
            
            # Create preview version
            preview_image = resize_image_for_preview(
                blank_image, 
                config.PREVIEW_MAX_SIZE
            )
            
            # Store the document
            pdf_doc = self.pdf1 if pdf_number == 1 else self.pdf2
            pdf_doc.file_path = None
            pdf_doc.is_blank = True
            pdf_doc.preview_image = preview_image
            pdf_doc.hires_image = blank_image
            
        except Exception as e:
            raise PDFLoadError(f"Failed to create blank page: {str(e)}")
    
    def set_orientation(self, pdf_number: int, orientation: Orientation) -> None:
        """Set PDF orientation"""
        pdf_doc = self.pdf1 if pdf_number == 1 else self.pdf2
        pdf_doc.orientation = orientation
    
    def get_preview_image(self, pdf_number: int) -> Optional[Image.Image]:
        """Get preview image for PDF"""
        pdf_doc = self.pdf1 if pdf_number == 1 else self.pdf2
        return pdf_doc.preview_image
    
    def load_hires_images(self) -> None:
        """Load high resolution images for processing"""
        try:
            # Load PDF1 hires if not already loaded
            if not self.pdf1.hires_image:
                if self.pdf1.is_blank:
                    self.pdf1.hires_image = create_blank_image(
                        config.A4_WIDTH_300DPI, 
                        config.A4_HEIGHT_300DPI
                    )
                elif self.pdf1.file_path:
                    images = self._convert_pdf_safe(
                        self.pdf1.file_path, 
                        dpi=config.EXPORT_DPI,
                        first_page=1, 
                        last_page=1
                    )
                    self.pdf1.hires_image = images[0] if images else None
            
            # Load PDF2 hires if not already loaded
            if not self.pdf2.hires_image:
                if self.pdf2.is_blank:
                    self.pdf2.hires_image = create_blank_image(
                        config.A4_WIDTH_300DPI, 
                        config.A4_HEIGHT_300DPI
                    )
                elif self.pdf2.file_path:
                    images = self._convert_pdf_safe(
                        self.pdf2.file_path, 
                        dpi=config.EXPORT_DPI,
                        first_page=1, 
                        last_page=1
                    )
                    self.pdf2.hires_image = images[0] if images else None
            
            # Validate images loaded
            if not self.pdf1.hires_image or not self.pdf2.hires_image:
                raise ImageProcessingError("Failed to load high resolution images")
            
            # Adjust blank page dimensions to match
            self._adjust_blank_page_dimensions()
            
        except Exception as e:
            raise PDFLoadError(f"Failed to load high resolution images: {str(e)}")
    
    def _adjust_blank_page_dimensions(self) -> None:
        """Adjust blank page dimensions to match PDF dimensions"""
        if self.pdf1.is_blank and not self.pdf2.is_blank:
            # Adjust PDF1 blank page to match PDF2 dimensions
            width, height = self.pdf2.hires_image.size
            self.pdf1.hires_image = create_blank_image(width, height)
            
        elif self.pdf2.is_blank and not self.pdf1.is_blank:
            # Adjust PDF2 blank page to match PDF1 dimensions
            width, height = self.pdf1.hires_image.size
            self.pdf2.hires_image = create_blank_image(width, height)
    
    def process_combination(self) -> CombinedDocument:
        """Process PDF combination"""
        if not self.pdf1.is_loaded or not self.pdf2.is_loaded:
            raise ValidationError("Both PDFs must be loaded before processing")
        
        try:
            # Load high resolution images
            self.load_hires_images()
            
            # Apply orientation transformations
            image1 = apply_orientation_transform(
                self.pdf1.hires_image, 
                self.pdf1.orientation.value
            )
            image2 = apply_orientation_transform(
                self.pdf2.hires_image, 
                self.pdf2.orientation.value
            )
            
            # Crop images into halves
            top_half_pdf1 = crop_image_half(image1, top_half=True)
            bottom_half_pdf1 = crop_image_half(image1, top_half=False)
            top_half_pdf2 = crop_image_half(image2, top_half=True)
            bottom_half_pdf2 = crop_image_half(image2, top_half=False)
            
            # Combine top halves (both top halves)
            combined_tops = combine_images_vertically(top_half_pdf1, top_half_pdf2)
            
            # Combine bottom halves (both bottom halves)
            combined_bottoms = combine_images_vertically(bottom_half_pdf1, bottom_half_pdf2)
            
            # Store combined images
            self.combined.top_combined = combined_tops
            self.combined.bottom_combined = combined_bottoms
            
            return self.combined
            
        except Exception as e:
            raise ImageProcessingError(f"Failed to process combination: {str(e)}")
    
    def export_combined_documents(self, save_directory: str, export_config: ExportConfig) -> Tuple[str, str]:
        """Export combined documents"""
        if not self.combined.is_ready:
            raise ValidationError("Combined documents are not ready for export")
        
        try:
            # Create file paths
            top_filename = export_config.get_full_filename(is_top=True)
            bottom_filename = export_config.get_full_filename(is_top=False)
            
            top_path = os.path.join(save_directory, top_filename)
            bottom_path = os.path.join(save_directory, bottom_filename)
            
            # Save images
            save_image_with_format(
                self.combined.top_combined,
                top_path,
                export_config.format_type,
                export_config.quality,
                export_config.dpi
            )
            
            save_image_with_format(
                self.combined.bottom_combined,
                bottom_path,
                export_config.format_type,
                export_config.quality,
                export_config.dpi
            )
            
            return top_path, bottom_path
            
        except Exception as e:
            raise ImageProcessingError(f"Failed to export documents: {str(e)}")
    
    def reset(self) -> None:
        """Reset processor state"""
        self.pdf1 = PDFDocument()
        self.pdf2 = PDFDocument()
        self.combined = CombinedDocument()
    
    def is_ready_to_process(self) -> bool:
        """Check if processor is ready to process"""
        return self.pdf1.is_loaded and self.pdf2.is_loaded 