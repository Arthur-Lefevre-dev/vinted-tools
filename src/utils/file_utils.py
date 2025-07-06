"""
File utilities for PDF Combiner application
"""

import os
import subprocess
import platform
from typing import Optional
from ..exceptions import FileNotFoundError


def validate_file_exists(file_path: str) -> bool:
    """Validate that file exists"""
    return os.path.exists(file_path) and os.path.isfile(file_path)


def validate_pdf_file(file_path: str) -> bool:
    """Validate that file is a PDF"""
    if not validate_file_exists(file_path):
        return False
    return file_path.lower().endswith('.pdf')


def get_file_size(file_path: str) -> Optional[int]:
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return None


def get_filename_without_extension(file_path: str) -> str:
    """Get filename without extension"""
    return os.path.splitext(os.path.basename(file_path))[0]


def ensure_directory_exists(directory_path: str) -> None:
    """Ensure directory exists, create if not"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def open_file_explorer(folder_path: str) -> bool:
    """Open file explorer at specified folder"""
    try:
        system = platform.system()
        if system == "Windows":
            subprocess.run(['explorer', folder_path], check=True)
        elif system == "Darwin":  # macOS
            subprocess.run(['open', folder_path], check=True)
        else:  # Linux
            subprocess.run(['xdg-open', folder_path], check=True)
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()


def get_unique_filename(base_path: str, filename: str) -> str:
    """Get unique filename by adding counter if file exists"""
    full_path = os.path.join(base_path, filename)
    if not os.path.exists(full_path):
        return filename
    
    name, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(full_path):
        new_filename = f"{name}_{counter}{ext}"
        full_path = os.path.join(base_path, new_filename)
        counter += 1
    
    return os.path.basename(full_path) 