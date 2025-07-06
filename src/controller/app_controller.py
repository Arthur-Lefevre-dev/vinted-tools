"""
Main application controller
"""

import threading
from typing import Optional
import os

from ..core import PDFProcessor
from ..ui import MainWindow
from ..models import Orientation, ExportConfig
from ..config import config
from ..exceptions import PDFCombinerError, PDFLoadError, ValidationError
from ..utils import (
    get_filename_without_extension,
    resize_image_for_preview,
    open_file_explorer
)


class AppController:
    """Main application controller - orchestrates the application"""
    
    def __init__(self):
        self.processor = PDFProcessor()
        self.window = MainWindow()
        self.processing = False
        
        # Connect UI callbacks
        self.setup_callbacks()
        
    def setup_callbacks(self) -> None:
        """Setup UI callbacks"""
        self.window.on_pdf_selected = self.handle_pdf_selected
        self.window.on_blank_selected = self.handle_blank_selected
        self.window.on_orientation_changed = self.handle_orientation_changed
        self.window.on_process_clicked = self.handle_process_clicked
        self.window.on_export_clicked = self.handle_export_clicked
        self.window.on_export_format_changed = self.handle_export_format_changed
        
    def handle_pdf_selected(self, pdf_number: int, file_path: str) -> None:
        """Handle PDF file selection"""
        try:
            # Load PDF
            self.processor.load_pdf_from_file(file_path, pdf_number)
            
            # Update UI
            filename = os.path.basename(file_path)
            self.window.update_pdf_info(pdf_number, filename, is_blank=False)
            
            # Update preview
            preview_image = self.processor.get_preview_image(pdf_number)
            if preview_image:
                # Resize for preview
                preview_resized = resize_image_for_preview(
                    preview_image, 
                    config.PREVIEW_MAX_SIZE
                )
                self.window.update_pdf_preview(pdf_number, preview_resized)
            
            # Update filename suggestions
            self.update_filename_suggestions()
            
        except PDFLoadError as e:
            self.window.show_error("Erreur de chargement", str(e))
        except Exception as e:
            self.window.show_error("Erreur", f"Erreur inattendue: {str(e)}")
    
    def handle_blank_selected(self, pdf_number: int) -> None:
        """Handle blank page selection"""
        try:
            # Load blank page
            self.processor.load_blank_page(pdf_number)
            
            # Update UI
            self.window.update_pdf_info(pdf_number, "", is_blank=True)
            
            # Update preview
            preview_image = self.processor.get_preview_image(pdf_number)
            if preview_image:
                self.window.update_pdf_preview(pdf_number, preview_image)
            
            # Update filename suggestions
            self.update_filename_suggestions()
            
        except PDFLoadError as e:
            self.window.show_error("Erreur de création", str(e))
        except Exception as e:
            self.window.show_error("Erreur", f"Erreur inattendue: {str(e)}")
    
    def handle_orientation_changed(self, pdf_number: int, orientation: str) -> None:
        """Handle orientation change"""
        try:
            # Convert string to Orientation enum
            orientation_enum = Orientation.PORTRAIT if orientation == "Portrait" else Orientation.LANDSCAPE
            
            # Update processor
            self.processor.set_orientation(pdf_number, orientation_enum)
            
            # Note: We don't update the preview here as it would require 
            # reloading the high-res image, which is expensive
            
        except Exception as e:
            self.window.show_error("Erreur", f"Erreur lors du changement d'orientation: {str(e)}")
    
    def handle_process_clicked(self) -> None:
        """Handle process button click"""
        if self.processing:
            return
        
        # Validate inputs
        if not self.processor.is_ready_to_process():
            self.window.show_warning(
                "Attention", 
                "Veuillez sélectionner deux éléments (PDF ou feuille blanche)"
            )
            return
        
        # Start processing in thread
        self.processing = True
        self.window.set_processing_state(True)
        self.window.update_progress(0)
        self.window.update_status("Démarrage du traitement...", config.INFO_COLOR)
        
        thread = threading.Thread(target=self.process_pdfs, daemon=config.THREAD_DAEMON)
        thread.start()
    
    def process_pdfs(self) -> None:
        """Process PDFs in background thread"""
        try:
            # Update progress
            self.window.root.after(0, lambda: self.window.update_progress(0.1))
            self.window.root.after(0, lambda: self.window.update_status(
                "Traitement des éléments...", config.INFO_COLOR
            ))
            
            # Process combination
            self.window.root.after(0, lambda: self.window.update_progress(0.5))
            self.window.root.after(0, lambda: self.window.update_status(
                "Découpage et combinaison des images...", config.INFO_COLOR
            ))
            
            combined_document = self.processor.process_combination()
            
            # Update progress
            self.window.root.after(0, lambda: self.window.update_progress(0.8))
            self.window.root.after(0, lambda: self.window.update_status(
                "Images combinées prêtes !", config.SUCCESS_COLOR
            ))
            
            # Update UI with results
            self.window.root.after(0, lambda: self.window.update_combined_previews(
                combined_document.top_combined,
                combined_document.bottom_combined
            ))
            
            # Enable export
            self.window.root.after(0, lambda: self.window.enable_export(True))
            
            # Finish processing
            self.window.root.after(0, lambda: self.finish_processing())
            
        except ValidationError as e:
            self.window.root.after(0, lambda: self.handle_processing_error(
                "Erreur de validation", str(e)
            ))
        except PDFCombinerError as e:
            self.window.root.after(0, lambda: self.handle_processing_error(
                "Erreur de traitement", str(e)
            ))
        except Exception as e:
            self.window.root.after(0, lambda: self.handle_processing_error(
                "Erreur", f"Erreur inattendue: {str(e)}"
            ))
    
    def handle_processing_error(self, title: str, message: str) -> None:
        """Handle processing error"""
        self.window.show_error(title, message)
        self.window.set_processing_state(False)
        self.window.update_progress(0)
        self.window.update_status(
            f"✗ Erreur lors du traitement: {message}", 
            config.ERROR_COLOR
        )
        self.window.enable_export(False)
        self.processing = False
    
    def finish_processing(self) -> None:
        """Finish processing and update UI"""
        self.processing = False
        self.window.set_processing_state(False)
        self.window.update_progress(1.0)
        self.window.update_status(
            "Combinaison terminée ! Vous pouvez maintenant exporter les fichiers.",
            config.SUCCESS_COLOR
        )
    
    def handle_export_clicked(self, export_config: ExportConfig, save_directory: str) -> None:
        """Handle export button click"""
        if not self.processor.combined.is_ready:
            self.window.show_warning("Attention", "Veuillez d'abord combiner les PDF")
            return
        
        try:
            # Update UI
            self.window.update_status(
                f"Création des {export_config.format_type} {export_config.dpi} DPI...",
                config.INFO_COLOR
            )
            
            # Export documents
            top_path, bottom_path = self.processor.export_combined_documents(
                save_directory, 
                export_config
            )
            
            # Update UI
            self.window.update_status(
                f"{export_config.format_type} {export_config.dpi} DPI exportés avec succès !",
                config.SUCCESS_COLOR
            )
            
            # Show success dialog
            self.window.show_success_dialog(
                format_type=export_config.format_type,
                top_filename=os.path.basename(top_path),
                bottom_filename=os.path.basename(bottom_path),
                save_directory=save_directory
            )
            
        except PDFCombinerError as e:
            self.window.show_error("Erreur d'export", str(e))
            self.window.update_status(
                f"✗ Erreur lors de l'export: {str(e)}",
                config.ERROR_COLOR
            )
        except Exception as e:
            self.window.show_error("Erreur", f"Erreur inattendue: {str(e)}")
            self.window.update_status(
                f"✗ Erreur lors de l'export: {str(e)}",
                config.ERROR_COLOR
            )
    
    def handle_export_format_changed(self, format_type: str) -> None:
        """Handle export format change"""
        # Update the combined document export format
        self.processor.combined.export_format = format_type
    
    def update_filename_suggestions(self) -> None:
        """Update filename suggestions based on loaded PDFs"""
        # Get PDF names
        pdf1_name = None
        pdf2_name = None
        
        if self.processor.pdf1.file_path:
            pdf1_name = get_filename_without_extension(self.processor.pdf1.file_path)
        elif self.processor.pdf1.is_blank:
            pdf1_name = "blank1"
        
        if self.processor.pdf2.file_path:
            pdf2_name = get_filename_without_extension(self.processor.pdf2.file_path)
        elif self.processor.pdf2.is_blank:
            pdf2_name = "blank2"
        
        # Update UI
        if pdf1_name and pdf2_name:
            self.window.export_panel.update_filename_suggestions(pdf1_name, pdf2_name)
    
    def run(self) -> None:
        """Start the application"""
        self.window.run()
    
    def shutdown(self) -> None:
        """Shutdown the application"""
        self.window.destroy() 