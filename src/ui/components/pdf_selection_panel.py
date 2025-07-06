"""
PDF Selection Panel component
"""

import customtkinter as ctk
from tkinter import filedialog
from typing import Optional, Callable
from PIL import Image

from ...config import config
from ...utils import convert_pil_to_ctk_image, get_filename_without_extension


class PDFSelectionPanel(ctk.CTkFrame):
    """Panel for PDF selection and preview"""
    
    def __init__(self, parent, on_pdf_selected: Optional[Callable] = None,
                 on_blank_selected: Optional[Callable] = None,
                 on_orientation_changed: Optional[Callable] = None):
        super().__init__(parent, corner_radius=8)
        
        self.on_pdf_selected = on_pdf_selected
        self.on_blank_selected = on_blank_selected
        self.on_orientation_changed = on_orientation_changed
        
        self.create_widgets()
        
    def create_widgets(self) -> None:
        """Create panel widgets"""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Sélection des fichiers PDF",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 15))
        
        # Container for PDF selection (side by side)
        self.pdfs_container = ctk.CTkFrame(self, fg_color="transparent")
        self.pdfs_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Create PDF selection widgets
        self.create_pdf_widgets()
        
    def create_pdf_widgets(self) -> None:
        """Create PDF selection widgets"""
        # PDF 1 (left side)
        self.pdf1_frame = ctk.CTkFrame(self.pdfs_container, corner_radius=8)
        self.pdf1_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.create_pdf_section(self.pdf1_frame, 1, "Premier PDF")
        
        # PDF 2 (right side)
        self.pdf2_frame = ctk.CTkFrame(self.pdfs_container, corner_radius=8)
        self.pdf2_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.create_pdf_section(self.pdf2_frame, 2, "Second PDF")
        
    def create_pdf_section(self, parent_frame: ctk.CTkFrame, pdf_number: int, title: str) -> None:
        """Create a PDF selection section"""
        # Title
        title_label = ctk.CTkLabel(
            parent_frame, 
            text=title, 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Info frame
        info_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=5)
        
        # File info label
        file_label = ctk.CTkLabel(
            info_frame, 
            text="Aucun fichier sélectionné", 
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50")
        )
        file_label.pack(side="left", padx=(0, 10))
        
        # Store reference to label
        if pdf_number == 1:
            self.pdf1_label = file_label
        else:
            self.pdf2_label = file_label
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        buttons_frame.pack(side="right", pady=10)
        
        # Browse button
        browse_button = ctk.CTkButton(
            buttons_frame,
            text="Parcourir",
            command=lambda: self._select_pdf(pdf_number),
            width=100,
            height=32,
            corner_radius=6
        )
        browse_button.pack(side="left", padx=(0, 5))
        
        # Blank page button
        blank_button = ctk.CTkButton(
            buttons_frame,
            text="Page blanche",
            command=lambda: self._select_blank(pdf_number),
            width=110,
            height=32,
            corner_radius=6
        )
        blank_button.pack(side="left")
        
        # Orientation frame
        orientation_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        orientation_frame.pack(fill="x", padx=15, pady=5)
        
        orientation_label = ctk.CTkLabel(
            orientation_frame,
            text="Orientation:",
            font=ctk.CTkFont(size=12)
        )
        orientation_label.pack(side="left", padx=(0, 10))
        
        # Orientation variable
        orientation_var = ctk.StringVar(value="Portrait")
        if pdf_number == 1:
            self.pdf1_orientation = orientation_var
        else:
            self.pdf2_orientation = orientation_var
        
        orientation_menu = ctk.CTkOptionMenu(
            orientation_frame,
            values=["Portrait", "Paysage"],
            variable=orientation_var,
            width=100,
            height=28,
            command=lambda value: self._orientation_changed(pdf_number, value)
        )
        orientation_menu.pack(side="left")
        
        # Preview frame
        preview_frame = ctk.CTkFrame(parent_frame, corner_radius=8)
        preview_frame.pack(fill="x", padx=15, pady=10)
        
        preview_title = ctk.CTkLabel(
            preview_frame,
            text="Aperçu",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        preview_title.pack(pady=(10, 5))
        
        # Preview image
        preview_image = ctk.CTkLabel(
            preview_frame,
            text="Pas d'aperçu\\ndisponible",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
            width=120,
            height=140
        )
        preview_image.pack(pady=(0, 10), padx=15)
        
        # Store reference to preview
        if pdf_number == 1:
            self.pdf1_preview = preview_image
        else:
            self.pdf2_preview = preview_image
    
    def _select_pdf(self, pdf_number: int) -> None:
        """Handle PDF file selection"""
        file_path = filedialog.askopenfilename(
            title=f"Sélectionner le PDF {pdf_number}",
            filetypes=config.PDF_FILE_TYPES
        )
        
        if file_path and self.on_pdf_selected:
            self.on_pdf_selected(pdf_number, file_path)
    
    def _select_blank(self, pdf_number: int) -> None:
        """Handle blank page selection"""
        if self.on_blank_selected:
            self.on_blank_selected(pdf_number)
    
    def _orientation_changed(self, pdf_number: int, orientation: str) -> None:
        """Handle orientation change"""
        if self.on_orientation_changed:
            self.on_orientation_changed(pdf_number, orientation)
    
    def update_info(self, pdf_number: int, filename: str, is_blank: bool = False) -> None:
        """Update PDF information display"""
        label = self.pdf1_label if pdf_number == 1 else self.pdf2_label
        
        if is_blank:
            label.configure(text="Page blanche sélectionnée")
        else:
            # Show just filename without extension
            display_name = get_filename_without_extension(filename)
            label.configure(text=display_name)
    
    def update_preview(self, pdf_number: int, preview_image: Optional[Image.Image]) -> None:
        """Update preview image"""
        preview_widget = self.pdf1_preview if pdf_number == 1 else self.pdf2_preview
        
        if preview_image:
            try:
                # Convert PIL image to CTk image
                ctk_image = convert_pil_to_ctk_image(preview_image)
                preview_widget.configure(image=ctk_image, text="")
            except Exception:
                # Fallback to text if image conversion fails
                preview_widget.configure(
                    image=None,
                    text="Aperçu\\ndisponible"
                )
        else:
            preview_widget.configure(
                image=None,
                text="Pas d'aperçu\\ndisponible"
            )
    
    def get_orientation(self, pdf_number: int) -> str:
        """Get current orientation for PDF"""
        if pdf_number == 1:
            return self.pdf1_orientation.get()
        else:
            return self.pdf2_orientation.get() 