"""
Export Panel component
"""

import customtkinter as ctk
from tkinter import filedialog
from typing import Optional, Callable

from ...config import config
from ...models import ExportConfig


class ExportPanel(ctk.CTkFrame):
    """Panel for export operations"""
    
    def __init__(self, parent, on_export_clicked: Optional[Callable] = None,
                 on_format_changed: Optional[Callable] = None):
        super().__init__(parent, corner_radius=8)
        
        self.on_export_clicked = on_export_clicked
        self.on_format_changed = on_format_changed
        
        self.create_widgets()
        
    def create_widgets(self) -> None:
        """Create panel widgets"""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Export et sauvegarde",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 15))
        
        # Export settings container
        settings_container = ctk.CTkFrame(self, fg_color="transparent")
        settings_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Format selection
        format_frame = ctk.CTkFrame(settings_container, corner_radius=8)
        format_frame.pack(fill="x", pady=(0, 15))
        
        format_title = ctk.CTkLabel(
            format_frame,
            text="Format d'export",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        format_title.pack(pady=(15, 10))
        
        self.format_var = ctk.StringVar(value=config.DEFAULT_EXPORT_FORMAT)
        self.format_menu = ctk.CTkOptionMenu(
            format_frame,
            values=list(config.SUPPORTED_FORMATS),
            variable=self.format_var,
            width=150,
            height=35,
            command=self._on_format_changed
        )
        self.format_menu.pack(pady=(0, 15))
        
        # Filename settings
        filename_frame = ctk.CTkFrame(settings_container, corner_radius=8)
        filename_frame.pack(fill="x", pady=(0, 15))
        
        filename_title = ctk.CTkLabel(
            filename_frame,
            text="Noms des fichiers",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        filename_title.pack(pady=(15, 10))
        
        # Filename inputs container
        filename_inputs = ctk.CTkFrame(filename_frame, fg_color="transparent")
        filename_inputs.pack(fill="x", padx=20, pady=(0, 15))
        
        # Top filename
        top_filename_frame = ctk.CTkFrame(filename_inputs, fg_color="transparent")
        top_filename_frame.pack(fill="x", pady=(0, 10))
        
        top_filename_label = ctk.CTkLabel(
            top_filename_frame,
            text="Fichier 1 (hauts):",
            font=ctk.CTkFont(size=12),
            width=120
        )
        top_filename_label.pack(side="left", padx=(0, 10))
        
        self.top_filename_entry = ctk.CTkEntry(
            top_filename_frame,
            placeholder_text=config.DEFAULT_TOP_FILENAME,
            width=200,
            height=30
        )
        self.top_filename_entry.pack(side="left", fill="x", expand=True)
        
        # Bottom filename
        bottom_filename_frame = ctk.CTkFrame(filename_inputs, fg_color="transparent")
        bottom_filename_frame.pack(fill="x")
        
        bottom_filename_label = ctk.CTkLabel(
            bottom_filename_frame,
            text="Fichier 2 (bas):",
            font=ctk.CTkFont(size=12),
            width=120
        )
        bottom_filename_label.pack(side="left", padx=(0, 10))
        
        self.bottom_filename_entry = ctk.CTkEntry(
            bottom_filename_frame,
            placeholder_text=config.DEFAULT_BOTTOM_FILENAME,
            width=200,
            height=30
        )
        self.bottom_filename_entry.pack(side="left", fill="x", expand=True)
        
        # Quality info
        quality_frame = ctk.CTkFrame(settings_container, corner_radius=8)
        quality_frame.pack(fill="x", pady=(0, 20))
        
        quality_title = ctk.CTkLabel(
            quality_frame,
            text="Qualité d'export",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        quality_title.pack(pady=(15, 5))
        
        quality_info = ctk.CTkLabel(
            quality_frame,
            text=f"Résolution: {config.EXPORT_DPI} DPI (qualité professionnelle)\\n"
                 f"Format: Haute résolution pour impression",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray40")
        )
        quality_info.pack(pady=(0, 15))
        
        # Export button
        self.export_button = ctk.CTkButton(
            self,
            text="Exporter les fichiers",
            command=self._on_export_clicked,
            width=200,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.export_button.pack(pady=(0, 20))
        
    def _on_format_changed(self, format_type: str) -> None:
        """Handle format change"""
        if self.on_format_changed:
            self.on_format_changed(format_type)
    
    def _on_export_clicked(self) -> None:
        """Handle export button click"""
        if not self.on_export_clicked:
            return
        
        # Get save directory
        save_directory = filedialog.askdirectory(
            title="Sélectionner le dossier de sauvegarde"
        )
        
        if not save_directory:
            return
        
        # Create export config
        export_config = ExportConfig(
            format_type=self.format_var.get(),
            quality=config.EXPORT_QUALITY,
            dpi=config.EXPORT_DPI,
            top_filename=self.top_filename_entry.get().strip() or config.DEFAULT_TOP_FILENAME,
            bottom_filename=self.bottom_filename_entry.get().strip() or config.DEFAULT_BOTTOM_FILENAME
        )
        
        # Call callback
        self.on_export_clicked(export_config, save_directory)
    
    def enable_export(self, enabled: bool) -> None:
        """Enable/disable export functionality"""
        state = "normal" if enabled else "disabled"
        self.export_button.configure(state=state)
        
        if enabled:
            self.export_button.configure(text="Exporter les fichiers")
        else:
            self.export_button.configure(text="Traitement requis")
    
    def update_filename_suggestions(self, pdf1_name: str = None, pdf2_name: str = None) -> None:
        """Update filename suggestions based on loaded PDFs"""
        if pdf1_name and pdf2_name:
            # Create combined filename suggestions
            base_name = f"{pdf1_name}_{pdf2_name}"
            
            # Update placeholders
            self.top_filename_entry.configure(placeholder_text=f"{base_name}_hauts")
            self.bottom_filename_entry.configure(placeholder_text=f"{base_name}_bas")
    
    def get_export_config(self) -> ExportConfig:
        """Get current export configuration"""
        return ExportConfig(
            format_type=self.format_var.get(),
            quality=config.EXPORT_QUALITY,
            dpi=config.EXPORT_DPI,
            top_filename=self.top_filename_entry.get().strip() or config.DEFAULT_TOP_FILENAME,
            bottom_filename=self.bottom_filename_entry.get().strip() or config.DEFAULT_BOTTOM_FILENAME
        )
    
    def reset_filenames(self) -> None:
        """Reset filename entries"""
        self.top_filename_entry.delete(0, 'end')
        self.bottom_filename_entry.delete(0, 'end')
        self.top_filename_entry.configure(placeholder_text=config.DEFAULT_TOP_FILENAME)
        self.bottom_filename_entry.configure(placeholder_text=config.DEFAULT_BOTTOM_FILENAME) 