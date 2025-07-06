"""
Success Dialog component
"""

import customtkinter as ctk
from typing import Optional

from ...config import config
from ...utils import open_file_explorer


class SuccessDialog:
    """Success dialog for export completion"""
    
    def __init__(self, parent, format_type: str, top_filename: str, 
                 bottom_filename: str, save_directory: str):
        self.parent = parent
        self.format_type = format_type
        self.top_filename = top_filename
        self.bottom_filename = bottom_filename
        self.save_directory = save_directory
        
        self.dialog = None
        
    def show(self) -> None:
        """Show the success dialog"""
        self.create_dialog()
        
    def create_dialog(self) -> None:
        """Create and show the success dialog"""
        # Create popup window
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Export Réussi")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Center the popup
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Create header
        self.create_header()
        
        # Create content
        self.create_content()
        
        # Create buttons
        self.create_buttons()
        
    def create_header(self) -> None:
        """Create dialog header"""
        header_frame = ctk.CTkFrame(
            self.dialog, 
            corner_radius=0, 
            height=80, 
            fg_color=config.SUCCESS_COLOR
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        success_icon = ctk.CTkLabel(
            header_frame,
            text="✓",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="white"
        )
        success_icon.pack(pady=20)
        
    def create_content(self) -> None:
        """Create dialog content"""
        # Main content frame
        content_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text=f"Export {self.format_type} Terminé !",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=config.SUCCESS_COLOR
        )
        title_label.pack(pady=(0, 20))
        
        # Files info
        self.create_files_info(content_frame)
        
        # Quality info
        self.create_quality_info(content_frame)
        
        # Location info
        self.create_location_info(content_frame)
        
    def create_files_info(self, parent) -> None:
        """Create files information section"""
        files_frame = ctk.CTkFrame(parent, corner_radius=8)
        files_frame.pack(fill="x", pady=10)
        
        files_title = ctk.CTkLabel(
            files_frame,
            text="Fichiers créés:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        files_title.pack(pady=(15, 5))
        
        file1_label = ctk.CTkLabel(
            files_frame,
            text=f"• {self.top_filename}",
            font=ctk.CTkFont(size=12)
        )
        file1_label.pack(pady=2)
        
        file2_label = ctk.CTkLabel(
            files_frame,
            text=f"• {self.bottom_filename}",
            font=ctk.CTkFont(size=12)
        )
        file2_label.pack(pady=(2, 15))
        
    def create_quality_info(self, parent) -> None:
        """Create quality information section"""
        quality_frame = ctk.CTkFrame(parent, corner_radius=8)
        quality_frame.pack(fill="x", pady=10)
        
        # Format specific info
        if self.format_type == "PDF":
            format_info = "Format: PDF vectoriel\\nDimensions originales préservées"
        else:
            format_info = "Format: PNG haute résolution\\nDimensions: Qualité professionnelle"
        
        quality_label = ctk.CTkLabel(
            quality_frame,
            text=f"Qualité: {config.EXPORT_DPI} DPI (professionnelle)\\n{format_info}",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        quality_label.pack(pady=15)
        
    def create_location_info(self, parent) -> None:
        """Create location information section"""
        location_frame = ctk.CTkFrame(parent, corner_radius=8)
        location_frame.pack(fill="x", pady=10)
        
        location_title = ctk.CTkLabel(
            location_frame,
            text="Emplacement:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        location_title.pack(pady=(10, 5))
        
        location_label = ctk.CTkLabel(
            location_frame,
            text=self.save_directory,
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray40")
        )
        location_label.pack(pady=(0, 10))
        
    def create_buttons(self) -> None:
        """Create dialog buttons"""
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Open folder button
        open_folder_btn = ctk.CTkButton(
            buttons_frame,
            text="Ouvrir Dossier",
            command=self._open_folder,
            width=150,
            height=35,
            corner_radius=6
        )
        open_folder_btn.pack(side="left", padx=(0, 10))
        
        # Close button
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Fermer",
            command=self._close_dialog,
            width=100,
            height=35,
            corner_radius=6,
            fg_color=config.SUCCESS_COLOR,
            hover_color=("lightgreen", "green")
        )
        close_btn.pack(side="right")
        
    def _open_folder(self) -> None:
        """Open folder in file explorer"""
        try:
            success = open_file_explorer(self.save_directory)
            if not success:
                # Show error message if opening folder fails
                error_dialog = ctk.CTkToplevel(self.dialog)
                error_dialog.title("Erreur")
                error_dialog.geometry("300x150")
                error_dialog.resizable(False, False)
                
                error_label = ctk.CTkLabel(
                    error_dialog,
                    text="Impossible d'ouvrir le dossier.\\nVeuillez naviguer manuellement vers:\\n" + 
                         self.save_directory,
                    font=ctk.CTkFont(size=11),
                    justify="center"
                )
                error_label.pack(pady=20)
                
                close_error_btn = ctk.CTkButton(
                    error_dialog,
                    text="OK",
                    command=error_dialog.destroy,
                    width=80,
                    height=30
                )
                close_error_btn.pack(pady=10)
                
        except Exception as e:
            print(f"Error opening folder: {e}")
    
    def _close_dialog(self) -> None:
        """Close the dialog"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None 