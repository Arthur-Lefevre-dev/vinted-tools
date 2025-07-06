"""
Processing Panel component
"""

import customtkinter as ctk
from typing import Optional, Callable, Tuple
from PIL import Image

from ...config import config
from ...utils import convert_pil_to_ctk_image, resize_image_for_preview


class ProcessingPanel(ctk.CTkFrame):
    """Panel for processing operations and preview"""
    
    def __init__(self, parent, on_process_clicked: Optional[Callable] = None):
        super().__init__(parent, corner_radius=8)
        
        self.on_process_clicked = on_process_clicked
        self.processing = False
        
        self.create_widgets()
        
    def create_widgets(self) -> None:
        """Create panel widgets"""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Traitement et aperçu",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 15))
        
        # Process button
        self.process_button = ctk.CTkButton(
            self,
            text="Combiner les PDF",
            command=self._on_process_clicked,
            width=200,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.process_button.pack(pady=(0, 20))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=400,
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Prêt à traiter",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(0, 20))
        
        # Combined previews container
        self.create_combined_previews()
        
    def create_combined_previews(self) -> None:
        """Create combined preview section"""
        # Preview title
        preview_title = ctk.CTkLabel(
            self,
            text="Aperçu du résultat",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        preview_title.pack(pady=(10, 15))
        
        # Preview container
        preview_container = ctk.CTkFrame(self, fg_color="transparent")
        preview_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Combined image 1 (left)
        combined1_frame = ctk.CTkFrame(preview_container, corner_radius=8)
        combined1_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        combined1_title = ctk.CTkLabel(
            combined1_frame,
            text="Fichier 1: Hauts combinés",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        combined1_title.pack(pady=(15, 10))
        
        self.combined1_preview = ctk.CTkLabel(
            combined1_frame,
            text="Pas d'aperçu\\ndisponible",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
            width=120,
            height=140
        )
        self.combined1_preview.pack(pady=(0, 15), padx=15)
        
        # Combined image 2 (right)
        combined2_frame = ctk.CTkFrame(preview_container, corner_radius=8)
        combined2_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        combined2_title = ctk.CTkLabel(
            combined2_frame,
            text="Fichier 2: Bas combinés",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        combined2_title.pack(pady=(15, 10))
        
        self.combined2_preview = ctk.CTkLabel(
            combined2_frame,
            text="Pas d'aperçu\\ndisponible",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
            width=120,
            height=140
        )
        self.combined2_preview.pack(pady=(0, 15), padx=15)
        
    def _on_process_clicked(self) -> None:
        """Handle process button click"""
        if self.on_process_clicked:
            self.on_process_clicked()
    
    def set_processing_state(self, processing: bool) -> None:
        """Set processing state"""
        self.processing = processing
        
        if processing:
            self.process_button.configure(
                state="disabled",
                text="Traitement en cours..."
            )
        else:
            self.process_button.configure(
                state="normal",
                text="Combiner les PDF"
            )
    
    def update_progress(self, progress: float) -> None:
        """Update progress bar"""
        self.progress_bar.set(progress)
    
    def update_status(self, message: str, color: Optional[Tuple[str, str]] = None) -> None:
        """Update status message"""
        self.status_label.configure(text=message)
        if color:
            self.status_label.configure(text_color=color)
    
    def update_combined_previews(self, top_image: Optional[Image.Image], 
                               bottom_image: Optional[Image.Image]) -> None:
        """Update combined preview images"""
        # Update top combined preview
        if top_image:
            try:
                # Resize for preview
                preview_image = resize_image_for_preview(top_image, config.PREVIEW_MAX_SIZE)
                ctk_image = convert_pil_to_ctk_image(preview_image)
                self.combined1_preview.configure(image=ctk_image, text="")
            except Exception:
                self.combined1_preview.configure(
                    image=None,
                    text="Aperçu\\ndisponible"
                )
        else:
            self.combined1_preview.configure(
                image=None,
                text="Pas d'aperçu\\ndisponible"
            )
        
        # Update bottom combined preview
        if bottom_image:
            try:
                # Resize for preview
                preview_image = resize_image_for_preview(bottom_image, config.PREVIEW_MAX_SIZE)
                ctk_image = convert_pil_to_ctk_image(preview_image)
                self.combined2_preview.configure(image=ctk_image, text="")
            except Exception:
                self.combined2_preview.configure(
                    image=None,
                    text="Aperçu\\ndisponible"
                )
        else:
            self.combined2_preview.configure(
                image=None,
                text="Pas d'aperçu\\ndisponible"
            )
    
    def reset_previews(self) -> None:
        """Reset combined previews"""
        self.combined1_preview.configure(
            image=None,
            text="Pas d'aperçu\\ndisponible"
        )
        self.combined2_preview.configure(
            image=None,
            text="Pas d'aperçu\\ndisponible"
        )
        
    def reset_progress(self) -> None:
        """Reset progress bar and status"""
        self.progress_bar.set(0)
        self.status_label.configure(
            text="Prêt à traiter",
            text_color=("white", "white")
        ) 