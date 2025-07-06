"""
Custom exceptions for PDF Combiner application
"""


class PDFCombinerError(Exception):
    """Base exception for PDF Combiner application"""
    pass


class PDFLoadError(PDFCombinerError):
    """Exception raised when PDF loading fails"""
    pass


class ImageProcessingError(PDFCombinerError):
    """Exception raised when image processing fails"""
    pass


class ExportError(PDFCombinerError):
    """Exception raised when export fails"""
    pass


class ValidationError(PDFCombinerError):
    """Exception raised when validation fails"""
    pass


class FileNotFoundError(PDFCombinerError):
    """Exception raised when file is not found"""
    pass


class UnsupportedFormatError(PDFCombinerError):
    """Exception raised when format is not supported"""
    pass 