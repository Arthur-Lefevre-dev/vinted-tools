"""
Configuration settings for PDF Combiner application
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class AppConfig:
    """Main application configuration"""
    
    # Window settings
    WINDOW_TITLE: str = "PDF Slice and Combine GODTOOL"  # 👈 Modifiez ici le titre
    WINDOW_SIZE: Tuple[int, int] = (1200, 900)
    WINDOW_ICON: str = "assets/icon.ico"  # 👈 Chemin vers l'icône (None si pas d'icône)
    
    # Theme settings
    APPEARANCE_MODE: str = "dark"  # "System", "Dark", "Light"
    COLOR_THEME: str = "blue"  # "blue", "green", "dark-blue"
    
    # Image processing settings
    PREVIEW_DPI: int = 100
    EXPORT_DPI: int = 300
    PREVIEW_MAX_SIZE: Tuple[int, int] = (120, 140)
    
    # A4 dimensions at 300 DPI
    A4_WIDTH_300DPI: int = 2480
    A4_HEIGHT_300DPI: int = 3508
    
    # Export settings
    DEFAULT_EXPORT_FORMAT: str = "PDF"
    SUPPORTED_FORMATS: Tuple[str, ...] = ("PDF", "PNG")
    EXPORT_QUALITY: int = 100
    
    # File dialog settings
    PDF_FILE_TYPES: Tuple[Tuple[str, str], ...] = (
        ("Fichiers PDF", "*.pdf"),
        ("Tous les fichiers", "*.*")
    )
    
    # UI Colors
    SUCCESS_COLOR: Tuple[str, str] = ("green", "lightgreen")
    ERROR_COLOR: Tuple[str, str] = ("red", "lightcoral")
    INFO_COLOR: Tuple[str, str] = ("blue", "lightblue")
    WARNING_COLOR: Tuple[str, str] = ("orange", "yellow")
    
    # Processing settings
    THREAD_DAEMON: bool = True
    
    # Default filenames
    DEFAULT_TOP_FILENAME: str = "tops_combined"
    DEFAULT_BOTTOM_FILENAME: str = "bottoms_combined"


# Global configuration instance
config = AppConfig() 