"""
Document models for PDF operations
"""

from dataclasses import dataclass
from typing import Optional, Tuple
from PIL import Image
from enum import Enum


class Orientation(Enum):
    """Document orientation enum"""
    PORTRAIT = "Portrait"
    LANDSCAPE = "Paysage"


@dataclass
class PDFDocument:
    """Model representing a PDF document with its properties"""
    file_path: Optional[str] = None
    is_blank: bool = False
    orientation: Orientation = Orientation.PORTRAIT
    preview_image: Optional[Image.Image] = None
    hires_image: Optional[Image.Image] = None
    
    @property
    def is_loaded(self) -> bool:
        """Check if document is loaded (either from file or as blank)"""
        return self.file_path is not None or self.is_blank
    
    @property
    def dimensions(self) -> Optional[Tuple[int, int]]:
        """Get document dimensions if available"""
        if self.hires_image:
            return self.hires_image.size
        elif self.preview_image:
            return self.preview_image.size
        return None


@dataclass
class CombinedDocument:
    """Model representing the combined document result"""
    top_combined: Optional[Image.Image] = None
    bottom_combined: Optional[Image.Image] = None
    export_format: str = "PDF"
    
    @property
    def is_ready(self) -> bool:
        """Check if combined document is ready for export"""
        return self.top_combined is not None and self.bottom_combined is not None
    
    def get_export_extension(self) -> str:
        """Get file extension for export format"""
        return self.export_format.lower()


@dataclass
class ExportConfig:
    """Configuration for document export"""
    format_type: str = "PDF"
    quality: int = 100
    dpi: int = 300
    top_filename: str = "tops_combined"
    bottom_filename: str = "bottoms_combined"
    
    def get_full_filename(self, is_top: bool) -> str:
        """Get full filename with extension"""
        base_name = self.top_filename if is_top else self.bottom_filename
        extension = self.format_type.lower()
        if not base_name.endswith(f'.{extension}'):
            base_name += f'.{extension}'
        return base_name 