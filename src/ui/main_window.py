"""
Main window for PDF Combiner application
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Callable

from ..config import config
from ..models import ExportConfig, Orientation
from ..exceptions import PDFCombinerError
from .components import PDFSelectionPanel, ProcessingPanel, ExportPanel, SuccessDialog


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_window()
        self.setup_theme()
        self.create_widgets()
        
        # Callbacks (to be set by controller)
        self.on_pdf_selected: Optional[Callable] = None
        self.on_blank_selected: Optional[Callable] = None
        self.on_orientation_changed: Optional[Callable] = None
        self.on_process_clicked: Optional[Callable] = None
        self.on_export_clicked: Optional[Callable] = None
        self.on_export_format_changed: Optional[Callable] = None
        
    def setup_window(self) -> None:
        """Setup main window properties"""
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_SIZE[0]}x{config.WINDOW_SIZE[1]}")
        
        # Set window icon if available
        if hasattr(config, 'WINDOW_ICON') and config.WINDOW_ICON:
            try:
                import os
                import sys
                
                # Check if running as compiled executable
                if getattr(sys, 'frozen', False):
                    # Running as compiled executable
                    base_path = sys._MEIPASS
                    icon_path = os.path.join(base_path, 'assets', 'icon.ico')
                else:
                    # Running as script
                    icon_path = config.WINDOW_ICON
                
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            except Exception:
                pass  # Ignore icon errors
        
    def setup_theme(self) -> None:
        """Setup application theme"""
        ctk.set_appearance_mode(config.APPEARANCE_MODE)
        ctk.set_default_color_theme(config.COLOR_THEME)
        
    def create_widgets(self) -> None:
        """Create main window widgets"""
        # Create main container with scrollbar
        self.main_container = ctk.CTkScrollableFrame(
            self.root, 
            corner_radius=0,
            fg_color="transparent",
            scrollbar_button_color=("gray70", "gray30"),
            scrollbar_button_hover_color=("gray60", "gray40")
        )
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Create header
        self.create_header()
        
        # Create main content frame
        self.workflow_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.workflow_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create panels
        self.create_panels()
        
    def create_header(self) -> None:
        """Create application header"""
        header_frame = ctk.CTkFrame(self.main_container, height=80, corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text=config.WINDOW_TITLE,  # 👈 Utilise la configuration centralisée
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Combinez les moitiés de deux PDF A4 • Export PDF/PNG • Qualité 300 DPI",
            font=ctk.CTkFont(size=13),
            text_color=("gray60", "gray40")
        )
        subtitle_label.pack(pady=(0, 15))
        
    def create_panels(self) -> None:
        """Create main application panels"""
        # PDF Selection Panel
        self.pdf_selection_panel = PDFSelectionPanel(
            self.workflow_frame,
            on_pdf_selected=self._on_pdf_selected,
            on_blank_selected=self._on_blank_selected,
            on_orientation_changed=self._on_orientation_changed
        )
        self.pdf_selection_panel.pack(fill="x", padx=20, pady=(20, 15))
        
        # Processing Panel
        self.processing_panel = ProcessingPanel(
            self.workflow_frame,
            on_process_clicked=self._on_process_clicked
        )
        self.processing_panel.pack(fill="x", padx=20, pady=15)
        
        # Export Panel
        self.export_panel = ExportPanel(
            self.workflow_frame,
            on_export_clicked=self._on_export_clicked,
            on_format_changed=self._on_export_format_changed
        )
        self.export_panel.pack(fill="x", padx=20, pady=(15, 20))
        
    def _on_pdf_selected(self, pdf_number: int, file_path: str) -> None:
        """Handle PDF selection"""
        if self.on_pdf_selected:
            self.on_pdf_selected(pdf_number, file_path)
    
    def _on_blank_selected(self, pdf_number: int) -> None:
        """Handle blank page selection"""
        if self.on_blank_selected:
            self.on_blank_selected(pdf_number)
    
    def _on_orientation_changed(self, pdf_number: int, orientation: str) -> None:
        """Handle orientation change"""
        if self.on_orientation_changed:
            self.on_orientation_changed(pdf_number, orientation)
    
    def _on_process_clicked(self) -> None:
        """Handle process button click"""
        if self.on_process_clicked:
            self.on_process_clicked()
    
    def _on_export_clicked(self, export_config: ExportConfig, save_directory: str) -> None:
        """Handle export button click"""
        if self.on_export_clicked:
            self.on_export_clicked(export_config, save_directory)
    
    def _on_export_format_changed(self, format_type: str) -> None:
        """Handle export format change"""
        if self.on_export_format_changed:
            self.on_export_format_changed(format_type)
    
    def update_pdf_preview(self, pdf_number: int, preview_image) -> None:
        """Update PDF preview image"""
        self.pdf_selection_panel.update_preview(pdf_number, preview_image)
    
    def update_pdf_info(self, pdf_number: int, filename: str, is_blank: bool = False) -> None:
        """Update PDF information display"""
        self.pdf_selection_panel.update_info(pdf_number, filename, is_blank)
    
    def update_combined_previews(self, top_image, bottom_image) -> None:
        """Update combined preview images"""
        self.processing_panel.update_combined_previews(top_image, bottom_image)
    
    def set_processing_state(self, processing: bool) -> None:
        """Set processing state"""
        self.processing_panel.set_processing_state(processing)
    
    def update_progress(self, progress: float) -> None:
        """Update progress bar"""
        self.processing_panel.update_progress(progress)
    
    def update_status(self, message: str, color: Optional[tuple] = None) -> None:
        """Update status message"""
        self.processing_panel.update_status(message, color)
    
    def enable_export(self, enabled: bool) -> None:
        """Enable/disable export functionality"""
        self.export_panel.enable_export(enabled)
    
    def show_success_dialog(self, format_type: str, top_filename: str, 
                          bottom_filename: str, save_directory: str) -> None:
        """Show success dialog"""
        dialog = SuccessDialog(
            self.root,
            format_type=format_type,
            top_filename=top_filename,
            bottom_filename=bottom_filename,
            save_directory=save_directory
        )
        dialog.show()
    
    def show_error(self, title: str, message: str) -> None:
        """Show error message"""
        messagebox.showerror(title, message)
    
    def show_warning(self, title: str, message: str) -> None:
        """Show warning message"""
        messagebox.showwarning(title, message)
    
    def run(self) -> None:
        """Start the application"""
        self.root.mainloop()
    
    def destroy(self) -> None:
        """Close the application"""
        self.root.destroy() 