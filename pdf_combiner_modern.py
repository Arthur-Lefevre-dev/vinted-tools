import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PIL import Image
import threading
import sys

try:
    from pdf2image import convert_from_path
except ImportError:
    print("pdf2image n'est pas installé. Veuillez installer les dépendances avec: pip install -r requirements.txt")
    sys.exit(1)

# Configure CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernPDFCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Combinateur PDF Professionnel")
        self.root.geometry("1200x900")
        
        # Variables for PDF files
        self.pdf1_path = None
        self.pdf2_path = None
        self.pdf1_image = None  # For preview (100 DPI)
        self.pdf2_image = None  # For preview (100 DPI)
        self.pdf1_hires = None  # For export (300 DPI)
        self.pdf2_hires = None  # For export (300 DPI)
        self.processing = False
        
        # Variables for blank page options
        self.pdf1_is_blank = False
        self.pdf2_is_blank = False
        
        # Variables for orientations
        self.pdf1_orientation = ctk.StringVar(value="Portrait")
        self.pdf2_orientation = ctk.StringVar(value="Portrait")
        
        # Variables for export
        self.combined_image1 = None
        self.combined_image2 = None
        self.export_ready = False
        self.export_format = ctk.StringVar(value="PDF")  # PDF or PNG
        
        # Create main container with scrollbar
        self.main_container = ctk.CTkScrollableFrame(
            root, 
            corner_radius=0,
            fg_color="transparent",
            scrollbar_button_color=("gray70", "gray30"),
            scrollbar_button_hover_color=("gray60", "gray40")
        )
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header Frame
        self.header_frame = ctk.CTkFrame(self.main_container, height=80, corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Title - clean and professional
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Combinateur PDF", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 5))
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Combinez les moitiés de deux PDF A4 • Export PDF/PNG • Qualité 300 DPI",
            font=ctk.CTkFont(size=13),
            text_color=("gray60", "gray40")
        )
        self.subtitle_label.pack(pady=(0, 15))
        
        # Main workflow frame - clean organization
        self.workflow_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.workflow_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # PDF Selection Section
        self.selection_frame = ctk.CTkFrame(self.workflow_frame, corner_radius=8)
        self.selection_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        self.selection_title = ctk.CTkLabel(
            self.selection_frame,
            text="Sélection des fichiers PDF",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.selection_title.pack(pady=(20, 15))
        
        # PDF Selection Container (side by side)
        self.pdfs_container = ctk.CTkFrame(self.selection_frame, fg_color="transparent")
        self.pdfs_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # PDF 1 Selection (left side)
        self.pdf1_frame = ctk.CTkFrame(self.pdfs_container, corner_radius=8)
        self.pdf1_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.pdf1_title = ctk.CTkLabel(
            self.pdf1_frame, 
            text="Premier PDF", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.pdf1_title.pack(pady=(20, 10))
        
        self.pdf1_info_frame = ctk.CTkFrame(self.pdf1_frame, fg_color="transparent")
        self.pdf1_info_frame.pack(fill="x", padx=15, pady=5)
        
        self.pdf1_label = ctk.CTkLabel(
            self.pdf1_info_frame, 
            text="Aucun fichier sélectionné", 
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50")
        )
        self.pdf1_label.pack(side="left", padx=(0, 10))
        
        # Buttons frame for PDF1
        self.pdf1_buttons_frame = ctk.CTkFrame(self.pdf1_info_frame, fg_color="transparent")
        self.pdf1_buttons_frame.pack(side="right", pady=10)
        
        self.pdf1_button = ctk.CTkButton(
            self.pdf1_buttons_frame,
            text="Parcourir",
            command=self.select_pdf1,
            width=100,
            height=32,
            corner_radius=6
        )
        self.pdf1_button.pack(side="left", padx=(0, 5))
        
        self.pdf1_blank_button = ctk.CTkButton(
            self.pdf1_buttons_frame,
            text="Page blanche",
            command=self.select_blank_pdf1,
            width=110,
            height=32,
            corner_radius=6
        )
        self.pdf1_blank_button.pack(side="left")
        
        # PDF 1 Orientation
        self.pdf1_orientation_frame = ctk.CTkFrame(self.pdf1_frame, fg_color="transparent")
        self.pdf1_orientation_frame.pack(fill="x", padx=15, pady=5)
        
        self.pdf1_orientation_label = ctk.CTkLabel(
            self.pdf1_orientation_frame,
            text="Orientation:",
            font=ctk.CTkFont(size=12)
        )
        self.pdf1_orientation_label.pack(side="left", padx=(0, 10))
        
        self.pdf1_orientation_menu = ctk.CTkOptionMenu(
            self.pdf1_orientation_frame,
            values=["Portrait", "Paysage"],
            variable=self.pdf1_orientation,
            width=100,
            height=28,
            command=self.update_pdf1_orientation
        )
        self.pdf1_orientation_menu.pack(side="left")
        
        # PDF 1 Preview
        self.pdf1_preview_frame = ctk.CTkFrame(self.pdf1_frame, corner_radius=8)
        self.pdf1_preview_frame.pack(fill="x", padx=15, pady=10)
        
        self.pdf1_preview_label = ctk.CTkLabel(
            self.pdf1_preview_frame,
            text="Aperçu",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.pdf1_preview_label.pack(pady=(10, 5))
        
        self.pdf1_preview_image = ctk.CTkLabel(
            self.pdf1_preview_frame,
            text="Pas d'aperçu\ndisponible",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
            width=120,
            height=140
        )
        self.pdf1_preview_image.pack(pady=(0, 10), padx=15)
        
        # PDF 2 Selection (right side)
        self.pdf2_frame = ctk.CTkFrame(self.pdfs_container, corner_radius=8)
        self.pdf2_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.pdf2_title = ctk.CTkLabel(
            self.pdf2_frame, 
            text="Second PDF", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.pdf2_title.pack(pady=(20, 10))
        
        self.pdf2_info_frame = ctk.CTkFrame(self.pdf2_frame, fg_color="transparent")
        self.pdf2_info_frame.pack(fill="x", padx=15, pady=5)
        
        self.pdf2_label = ctk.CTkLabel(
            self.pdf2_info_frame, 
            text="Aucun fichier sélectionné", 
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50")
        )
        self.pdf2_label.pack(side="left", padx=(0, 10))
        
        # Buttons frame for PDF2
        self.pdf2_buttons_frame = ctk.CTkFrame(self.pdf2_info_frame, fg_color="transparent")
        self.pdf2_buttons_frame.pack(side="right", pady=10)
        
        self.pdf2_button = ctk.CTkButton(
            self.pdf2_buttons_frame,
            text="Parcourir",
            command=self.select_pdf2,
            width=100,
            height=32,
            corner_radius=6
        )
        self.pdf2_button.pack(side="left", padx=(0, 5))
        
        self.pdf2_blank_button = ctk.CTkButton(
            self.pdf2_buttons_frame,
            text="Page blanche",
            command=self.select_blank_pdf2,
            width=110,
            height=32,
            corner_radius=6
        )
        self.pdf2_blank_button.pack(side="left")
        
        # PDF 2 Orientation
        self.pdf2_orientation_frame = ctk.CTkFrame(self.pdf2_frame, fg_color="transparent")
        self.pdf2_orientation_frame.pack(fill="x", padx=15, pady=5)
        
        self.pdf2_orientation_label = ctk.CTkLabel(
            self.pdf2_orientation_frame,
            text="Orientation:",
            font=ctk.CTkFont(size=12)
        )
        self.pdf2_orientation_label.pack(side="left", padx=(0, 10))
        
        self.pdf2_orientation_menu = ctk.CTkOptionMenu(
            self.pdf2_orientation_frame,
            values=["Portrait", "Paysage"],
            variable=self.pdf2_orientation,
            width=100,
            height=28,
            command=self.update_pdf2_orientation
        )
        self.pdf2_orientation_menu.pack(side="left")
        
        # PDF 2 Preview
        self.pdf2_preview_frame = ctk.CTkFrame(self.pdf2_frame, corner_radius=8)
        self.pdf2_preview_frame.pack(fill="x", padx=15, pady=10)
        
        self.pdf2_preview_label = ctk.CTkLabel(
            self.pdf2_preview_frame,
            text="Aperçu",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.pdf2_preview_label.pack(pady=(10, 5))
        
        self.pdf2_preview_image = ctk.CTkLabel(
            self.pdf2_preview_frame,
            text="Pas d'aperçu\ndisponible",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
            width=120,
            height=140
        )
        self.pdf2_preview_image.pack(pady=(0, 10), padx=15)
        
        # Combination Section
        self.combination_frame = ctk.CTkFrame(self.workflow_frame, corner_radius=8)
        self.combination_frame.pack(fill="x", padx=20, pady=15)
        
        self.combination_title = ctk.CTkLabel(
            self.combination_frame,
            text="Combinaison des fichiers",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.combination_title.pack(pady=(20, 15))
        
        # Process button
        self.process_button = ctk.CTkButton(
            self.combination_frame,
            text="Combiner les PDF",
            command=self.process_pdfs_threaded,
            width=200,
            height=45,
            corner_radius=8,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.process_button.pack(pady=(0, 15))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.combination_frame,
            width=400,
            height=8,
            corner_radius=4
        )
        self.progress_bar.pack(pady=(0, 15))
        self.progress_bar.set(0)
        
        # Preview results frame
        self.preview_main_frame = ctk.CTkFrame(self.combination_frame, corner_radius=8, fg_color="transparent")
        self.preview_main_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.preview_title = ctk.CTkLabel(
            self.preview_main_frame,
            text="Aperçu des résultats",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.preview_title.pack(pady=(15, 10))
        
        self.preview_container = ctk.CTkFrame(self.preview_main_frame, fg_color="transparent")
        self.preview_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Combined results preview frames
        self.combined1_frame = ctk.CTkFrame(self.preview_container, corner_radius=8)
        self.combined1_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.combined1_title = ctk.CTkLabel(
            self.combined1_frame,
            text="Résultat 1\n(PDF1 Haut + PDF2 Haut)",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.combined1_title.pack(pady=(15, 5))
        
        self.combined1_image = ctk.CTkLabel(
            self.combined1_frame,
            text="Combinez d'abord\nles PDF",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
            width=140,
            height=180
        )
        self.combined1_image.pack(pady=10, padx=15)
        
        self.combined2_frame = ctk.CTkFrame(self.preview_container, corner_radius=8)
        self.combined2_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.combined2_title = ctk.CTkLabel(
            self.combined2_frame,
            text="Résultat 2\n(PDF1 Bas + PDF2 Bas)",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.combined2_title.pack(pady=(15, 5))
        
        self.combined2_image = ctk.CTkLabel(
            self.combined2_frame,
            text="Combinez d'abord\nles PDF",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
            width=140,
            height=180
        )
        self.combined2_image.pack(pady=10, padx=15)
        
        # Export Section
        self.export_section_frame = ctk.CTkFrame(self.workflow_frame, corner_radius=8)
        self.export_section_frame.pack(fill="x", padx=20, pady=15)
        
        self.export_section_title = ctk.CTkLabel(
            self.export_section_frame,
            text="Export des fichiers",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.export_section_title.pack(pady=(20, 15))
        
        # Export Frame
        self.export_frame = ctk.CTkFrame(self.export_section_frame, corner_radius=8, fg_color="transparent")
        self.export_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Export options
        self.export_options_frame = ctk.CTkFrame(self.export_frame, fg_color="transparent")
        self.export_options_frame.pack(fill="x", padx=0, pady=10)
        
        # Export format selection
        self.format_frame = ctk.CTkFrame(self.export_options_frame, fg_color="transparent")
        self.format_frame.pack(fill="x", pady=10)
        
        self.format_label = ctk.CTkLabel(
            self.format_frame,
            text="Format d'export:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.format_label.pack(side="left", padx=(0, 10))
        
        self.format_menu = ctk.CTkOptionMenu(
            self.format_frame,
            values=["PDF", "PNG"],
            variable=self.export_format,
            width=100,
            height=32,
            command=self.update_export_format
        )
        self.format_menu.pack(side="left", padx=(0, 20))
        
        self.format_info = ctk.CTkLabel(
            self.format_frame,
            text="PDF: Document vectoriel • PNG: Image haute résolution",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray40")
        )
        self.format_info.pack(side="left")
        
        # File name entries
        self.filename1_frame = ctk.CTkFrame(self.export_options_frame, fg_color="transparent")
        self.filename1_frame.pack(fill="x", pady=5)
        
        self.filename1_label = ctk.CTkLabel(
            self.filename1_frame,
            text="Nom fichier 1:",
            font=ctk.CTkFont(size=12),
            width=100
        )
        self.filename1_label.pack(side="left", padx=(0, 10))
        
        self.filename1_entry = ctk.CTkEntry(
            self.filename1_frame,
            placeholder_text="tops_combined.pdf",
            width=250,
            height=32,
            border_width=2,
            corner_radius=6
        )
        self.filename1_entry.pack(side="left", padx=(0, 10))
        
        self.filename2_frame = ctk.CTkFrame(self.export_options_frame, fg_color="transparent")
        self.filename2_frame.pack(fill="x", pady=5)
        
        self.filename2_label = ctk.CTkLabel(
            self.filename2_frame,
            text="Nom fichier 2:",
            font=ctk.CTkFont(size=12),
            width=100
        )
        self.filename2_label.pack(side="left", padx=(0, 10))
        
        self.filename2_entry = ctk.CTkEntry(
            self.filename2_frame,
            placeholder_text="bottoms_combined.pdf",
            width=250,
            height=32,
            border_width=2,
            corner_radius=6
        )
        self.filename2_entry.pack(side="left", padx=(0, 10))
        
        # Export button
        self.export_button = ctk.CTkButton(
            self.export_frame,
            text="Exporter les fichiers",
            command=self.export_images,
            width=250,
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("green", "darkgreen"),
            hover_color=("lightgreen", "green"),
            state="disabled"
        )
        self.export_button.pack(pady=25)
        
        # Status and Settings Frame
        self.status_frame = ctk.CTkFrame(self.workflow_frame, corner_radius=8)
        self.status_frame.pack(fill="x", padx=20, pady=(15, 20))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Sélectionnez deux fichiers PDF pour commencer",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray40")
        )
        self.status_label.pack(pady=15)
        
        # Theme toggle
        self.theme_frame = ctk.CTkFrame(self.status_frame, fg_color="transparent")
        self.theme_frame.pack(pady=(0, 15))
        
        self.theme_label = ctk.CTkLabel(
            self.theme_frame,
            text="Thème:",
            font=ctk.CTkFont(size=12)
        )
        self.theme_label.pack(side="left", padx=(0, 10))
        
        self.theme_switch = ctk.CTkSwitch(
            self.theme_frame,
            text="Sombre",
            command=self.toggle_theme,
            width=60,
            height=24
        )
        self.theme_switch.pack(side="left")
        self.theme_switch.select()  # Start with dark theme
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="Sombre")
        else:
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="Clair")
            
    def select_pdf1(self):
        """Select first PDF file"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner le premier PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.pdf1_path = file_path
            self.pdf1_is_blank = False
            filename = os.path.basename(file_path)
            self.pdf1_label.configure(text=f"✓ {filename}", text_color=("green", "lightgreen"))
            self.status_label.configure(text="Chargement de l'aperçu...")
            self.root.update()
            
            # Load preview in thread
            threading.Thread(target=self.load_pdf_preview, args=(file_path, 1), daemon=True).start()
            
    def select_pdf2(self):
        """Select second PDF file"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner le second PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.pdf2_path = file_path
            self.pdf2_is_blank = False
            filename = os.path.basename(file_path)
            self.pdf2_label.configure(text=f"✓ {filename}", text_color=("green", "lightgreen"))
            self.status_label.configure(text="Chargement de l'aperçu...")
            self.root.update()
            
            # Load preview in thread
            threading.Thread(target=self.load_pdf_preview, args=(file_path, 2), daemon=True).start()
            
    def select_blank_pdf1(self):
        """Select blank page for first PDF"""
        self.pdf1_path = None
        self.pdf1_is_blank = True
        self.pdf1_label.configure(text="✓ Page blanche sélectionnée", text_color=("green", "lightgreen"))
        # Create and show blank preview
        self.create_blank_preview(1)
        self.check_ready_to_process()
        self.update_filename_suggestions()
        
    def select_blank_pdf2(self):
        """Select blank page for second PDF"""
        self.pdf2_path = None
        self.pdf2_is_blank = True
        self.pdf2_label.configure(text="✓ Page blanche sélectionnée", text_color=("green", "lightgreen"))
        # Create and show blank preview
        self.create_blank_preview(2)
        self.check_ready_to_process()
        self.update_filename_suggestions()
        
    def create_blank_preview(self, pdf_number):
        """Create a blank preview for the specified PDF"""
        # Create a white image for preview
        blank_image = Image.new('RGB', (120, 140), 'white')
        
        # Store blank image
        if pdf_number == 1:
            self.pdf1_image = blank_image
        else:
            self.pdf2_image = blank_image
        
        # Create CTkImage for preview
        ctk_image = ctk.CTkImage(light_image=blank_image, dark_image=blank_image, size=(120, 140))
        
        # Update preview
        self.update_preview(ctk_image, pdf_number)
        
    def create_blank_page(self, width, height):
        """Create a blank page with specified dimensions"""
        return Image.new('RGB', (width, height), 'white')
            
    def load_pdf_preview(self, pdf_path, pdf_number):
        """Load and display PDF preview (BASSE RÉSOLUTION pour aperçu seulement)"""
        try:
            # Convert first page of PDF to image (100 DPI pour aperçu rapide)
            images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=100)
            if images:
                image = images[0]
                
                # Store PREVIEW image (100 DPI - PAS pour l'export final)
                if pdf_number == 1:
                    self.pdf1_image = image
                else:
                    self.pdf2_image = image
                
                # Apply orientation to preview
                if pdf_number == 1:
                    oriented_image = self.apply_orientation(image, self.pdf1_orientation.get())
                else:
                    oriented_image = self.apply_orientation(image, self.pdf2_orientation.get())
                
                # Create thumbnail for preview
                preview_image = oriented_image.copy()
                preview_image.thumbnail((120, 140), Image.Resampling.LANCZOS)
                
                # Convert to CTkImage for better compatibility
                ctk_image = ctk.CTkImage(light_image=preview_image, dark_image=preview_image, size=(120, 140))
                
                # Update preview on main thread
                self.root.after(0, lambda: self.update_preview(ctk_image, pdf_number))
                
        except Exception as e:
            error_msg = f"✗ Erreur lors du chargement du PDF {pdf_number}: {str(e)}"
            self.root.after(0, lambda: self.status_label.configure(text=error_msg, text_color=("red", "lightcoral")))
            
    def update_preview(self, ctk_image, pdf_number):
        """Update preview image on main thread"""
        if pdf_number == 1:
            self.pdf1_preview_image.configure(image=ctk_image, text="")
            self.pdf1_preview_image.image = ctk_image  # Keep a reference
        else:
            self.pdf2_preview_image.configure(image=ctk_image, text="")
            self.pdf2_preview_image.image = ctk_image  # Keep a reference
            
        self.check_ready_to_process()
        
    def update_pdf1_orientation(self, value):
        """Update PDF1 preview when orientation changes"""
        if self.pdf1_image:
            self.refresh_preview(1)
            
    def update_pdf2_orientation(self, value):
        """Update PDF2 preview when orientation changes"""
        if self.pdf2_image:
            self.refresh_preview(2)
            
    def refresh_preview(self, pdf_number):
        """Refresh preview with current orientation"""
        if pdf_number == 1 and self.pdf1_image:
            # Apply orientation to preview
            image = self.apply_orientation(self.pdf1_image, self.pdf1_orientation.get())
            image_copy = image.copy()
            image_copy.thumbnail((120, 140), Image.Resampling.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=image_copy, dark_image=image_copy, size=(120, 140))
            self.pdf1_preview_image.configure(image=ctk_image, text="")
            self.pdf1_preview_image.image = ctk_image
            
        elif pdf_number == 2 and self.pdf2_image:
            # Apply orientation to preview
            image = self.apply_orientation(self.pdf2_image, self.pdf2_orientation.get())
            image_copy = image.copy()
            image_copy.thumbnail((120, 140), Image.Resampling.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=image_copy, dark_image=image_copy, size=(120, 140))
            self.pdf2_preview_image.configure(image=ctk_image, text="")
            self.pdf2_preview_image.image = ctk_image
        
    def update_combined_previews(self, combined_image1, combined_image2):
        """Update combined results preview"""
        try:
            # Create thumbnails for combined images
            thumb1 = combined_image1.copy()
            thumb1.thumbnail((140, 180), Image.Resampling.LANCZOS)
            ctk_thumb1 = ctk.CTkImage(light_image=thumb1, dark_image=thumb1, size=(140, 180))
            
            thumb2 = combined_image2.copy()
            thumb2.thumbnail((140, 180), Image.Resampling.LANCZOS)
            ctk_thumb2 = ctk.CTkImage(light_image=thumb2, dark_image=thumb2, size=(140, 180))
            
            # Update combined previews
            self.combined1_image.configure(image=ctk_thumb1, text="")
            self.combined1_image.image = ctk_thumb1
            
            self.combined2_image.configure(image=ctk_thumb2, text="")
            self.combined2_image.image = ctk_thumb2
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour des aperçus: {e}")
        
    def check_ready_to_process(self):
        """Check if both PDFs are loaded and enable process button"""
        # Check if both inputs are ready (either PDF files or blank pages)
        pdf1_ready = self.pdf1_path is not None or self.pdf1_is_blank
        pdf2_ready = self.pdf2_path is not None or self.pdf2_is_blank
        
        if pdf1_ready and pdf2_ready:
            self.process_button.configure(state="normal")
            self.status_label.configure(
                text="Prêt à combiner !",
                text_color=("green", "lightgreen")
            )
            # Update filename suggestions
            self.update_filename_suggestions()
        else:
            self.process_button.configure(state="disabled")
            
    def update_filename_suggestions(self):
        """Update filename suggestions based on selected PDFs"""
        # Check if both inputs are ready (either PDF files or blank pages)
        pdf1_ready = self.pdf1_path is not None or self.pdf1_is_blank
        pdf2_ready = self.pdf2_path is not None or self.pdf2_is_blank
        
        if pdf1_ready and pdf2_ready:
            # Get base names for filenames
            if self.pdf1_is_blank:
                base1 = "blank"
            else:
                base1 = os.path.splitext(os.path.basename(self.pdf1_path))[0]
                
            if self.pdf2_is_blank:
                base2 = "blank"
            else:
                base2 = os.path.splitext(os.path.basename(self.pdf2_path))[0]
            
            # Get current format
            format_ext = self.export_format.get().lower()
            
            # Set placeholder text - NOUVELLE LOGIQUE CORRIGÉE
            self.filename1_entry.configure(placeholder_text=f"{base1}_top_{base2}_top.{format_ext}")
            self.filename2_entry.configure(placeholder_text=f"{base1}_bottom_{base2}_bottom.{format_ext}")
            
    def update_export_format(self, value):
        """Update export format and filename suggestions"""
        # Update filename suggestions with new format
        self.update_filename_suggestions()
        
        # Update export button text
        if value == "PDF":
            self.export_button.configure(text="Exporter en PDF")
        else:
            self.export_button.configure(text="Exporter en PNG")
            
    def process_pdfs_threaded(self):
        """Start PDF processing in a separate thread"""
        if self.processing:
            return
            
        self.processing = True
        self.process_button.configure(state="disabled", text="Traitement en cours...")
        self.export_button.configure(state="disabled")
        self.progress_bar.set(0)
        
        # Start processing in thread
        threading.Thread(target=self.process_pdfs, daemon=True).start()
        
    def process_pdfs(self):
        """Process the PDFs and create combined images"""
        # Check if both inputs are ready (either PDF files or blank pages)
        pdf1_ready = self.pdf1_path is not None or self.pdf1_is_blank
        pdf2_ready = self.pdf2_path is not None or self.pdf2_is_blank
        
        if not pdf1_ready or not pdf2_ready:
            self.root.after(0, lambda: messagebox.showwarning("Attention", "Veuillez sélectionner deux éléments (PDF ou feuille blanche)"))
            self.processing = False
            return
            
        try:
            # Update progress
            self.root.after(0, lambda: self.progress_bar.set(0.1))
            self.root.after(0, lambda: self.status_label.configure(text="Traitement des éléments..."))
            
            # Handle PDF 1 (either file or blank page)
            if self.pdf1_is_blank:
                self.root.after(0, lambda: self.status_label.configure(text="Création de la feuille blanche 1..."))
                # Create a standard A4 page (2480x3508 pixels at 300 DPI)
                self.pdf1_hires = self.create_blank_page(2480, 3508)
            else:
                self.root.after(0, lambda: self.status_label.configure(text="Rechargement PDF 1 en 300 DPI haute qualité..."))
                images1 = convert_from_path(self.pdf1_path, first_page=1, last_page=1, dpi=300)
                self.pdf1_hires = images1[0] if images1 else None
                
            self.root.after(0, lambda: self.progress_bar.set(0.3))
            
            # Handle PDF 2 (either file or blank page)
            if self.pdf2_is_blank:
                self.root.after(0, lambda: self.status_label.configure(text="Création de la feuille blanche 2..."))
                # Create a standard A4 page (2480x3508 pixels at 300 DPI)
                self.pdf2_hires = self.create_blank_page(2480, 3508)
            else:
                self.root.after(0, lambda: self.status_label.configure(text="Rechargement PDF 2 en 300 DPI haute qualité..."))
                images2 = convert_from_path(self.pdf2_path, first_page=1, last_page=1, dpi=300)
                self.pdf2_hires = images2[0] if images2 else None
                
            self.root.after(0, lambda: self.progress_bar.set(0.5))
            
            if not self.pdf1_hires or not self.pdf2_hires:
                raise Exception("Impossible de créer les images haute résolution")
                
            # Adjust dimensions for blank pages if needed
            if self.pdf1_is_blank and not self.pdf2_is_blank:
                # Adjust blank page to match PDF dimensions
                width2, height2 = self.pdf2_hires.size
                self.pdf1_hires = self.create_blank_page(width2, height2)
            elif self.pdf2_is_blank and not self.pdf1_is_blank:
                # Adjust blank page to match PDF dimensions
                width1, height1 = self.pdf1_hires.size
                self.pdf2_hires = self.create_blank_page(width1, height1)
                
            self.root.after(0, lambda: self.status_label.configure(text="Découpage et combinaison des images..."))
            
            # Get image dimensions and orientations (UTILISER les images haute résolution)
            width1, height1 = self.pdf1_hires.size
            width2, height2 = self.pdf2_hires.size
            
            # Apply orientation adjustments (UTILISER les images haute résolution)
            image1 = self.apply_orientation(self.pdf1_hires, self.pdf1_orientation.get())
            image2 = self.apply_orientation(self.pdf2_hires, self.pdf2_orientation.get())
            
            # Get adjusted dimensions
            width1, height1 = image1.size
            width2, height2 = image2.size
            
            # Create combined images - NOUVELLE LOGIQUE CORRIGÉE
            # Image 1: Top half of PDF1 + Top half of PDF2
            top_half_pdf1 = image1.crop((0, 0, width1, height1 // 2))
            top_half_pdf2 = image2.crop((0, 0, width2, height2 // 2))
            
            # Resize to match width if needed
            target_width = max(width1, width2)
            if top_half_pdf1.width != target_width:
                top_half_pdf1 = top_half_pdf1.resize((target_width, top_half_pdf1.height), Image.Resampling.LANCZOS)
            if top_half_pdf2.width != target_width:
                top_half_pdf2 = top_half_pdf2.resize((target_width, top_half_pdf2.height), Image.Resampling.LANCZOS)
            
            # Create first combined image with high quality (Both TOP halves)
            combined_image1 = Image.new('RGB', (target_width, top_half_pdf1.height + top_half_pdf2.height), 'white')
            combined_image1.paste(top_half_pdf1, (0, 0))
            combined_image1.paste(top_half_pdf2, (0, top_half_pdf1.height))
            
            self.root.after(0, lambda: self.progress_bar.set(0.7))
            
            # Image 2: Bottom half of PDF1 + Bottom half of PDF2
            bottom_half_pdf1 = image1.crop((0, height1 // 2, width1, height1))
            bottom_half_pdf2 = image2.crop((0, height2 // 2, width2, height2))
            
            # Resize to match width if needed with high quality
            if bottom_half_pdf1.width != target_width:
                bottom_half_pdf1 = bottom_half_pdf1.resize((target_width, bottom_half_pdf1.height), Image.Resampling.LANCZOS)
            if bottom_half_pdf2.width != target_width:
                bottom_half_pdf2 = bottom_half_pdf2.resize((target_width, bottom_half_pdf2.height), Image.Resampling.LANCZOS)
            
            # Create second combined image with high quality (Both BOTTOM halves)
            combined_image2 = Image.new('RGB', (target_width, bottom_half_pdf1.height + bottom_half_pdf2.height), 'white')
            combined_image2.paste(bottom_half_pdf1, (0, 0))
            combined_image2.paste(bottom_half_pdf2, (0, bottom_half_pdf1.height))
            
            self.root.after(0, lambda: self.progress_bar.set(0.8))
            self.root.after(0, lambda: self.status_label.configure(text="Images combinées prêtes !"))
            
            # Store combined images for export
            self.combined_image1 = combined_image1
            self.combined_image2 = combined_image2
            self.export_ready = True
            
            # Update combined previews
            self.root.after(0, lambda: self.update_combined_previews(combined_image1, combined_image2))
            
            # Enable export button
            self.root.after(0, lambda: self.export_button.configure(state="normal"))
            
            # Finish processing
            self.root.after(0, lambda: self.finish_processing())
            
        except Exception as e:
            error_msg = f"✗ Erreur lors du traitement: {str(e)}"
            self.root.after(0, lambda: self.status_label.configure(text=error_msg, text_color=("red", "lightcoral")))
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur lors du traitement: {str(e)}"))
            self.processing = False
            self.root.after(0, lambda: self.process_button.configure(state="normal", text="Combiner les PDF"))
            self.root.after(0, lambda: self.export_button.configure(state="disabled"))
            self.root.after(0, lambda: self.progress_bar.set(0))
            
    def apply_orientation(self, image, orientation):
        """Apply orientation to image"""
        if orientation == "Paysage":
            # Rotate 90 degrees for landscape
            return image.rotate(90, expand=True)
        return image  # Portrait - no rotation needed
        

        
    def finish_processing(self):
        """Finish processing and reset UI"""
        self.processing = False
        self.process_button.configure(state="normal", text="Combiner les PDF")
        self.progress_bar.set(1.0)
        self.status_label.configure(
            text="Combinaison terminée ! Vous pouvez maintenant exporter les fichiers.",
            text_color=("green", "lightgreen")
        )
        
    def export_images(self):
        """Export the combined images in selected format"""
        if not self.export_ready or not self.combined_image1 or not self.combined_image2:
            messagebox.showwarning("Attention", "Veuillez d'abord combiner les PDF")
            return
            
        try:
            # Ask user where to save the files
            save_dir = filedialog.askdirectory(title="Sélectionner le dossier de sauvegarde")
            if not save_dir:
                return
                
            # Get filename from entries or use defaults
            filename1 = self.filename1_entry.get().strip()
            filename2 = self.filename2_entry.get().strip()
            
            format_type = self.export_format.get()
            format_ext = format_type.lower()
            
            if not filename1:
                filename1 = self.filename1_entry.cget("placeholder_text") or f"tops_combined.{format_ext}"
            if not filename2:
                filename2 = self.filename2_entry.cget("placeholder_text") or f"bottoms_combined.{format_ext}"
                
            # Ensure correct extension
            if not filename1.lower().endswith(f'.{format_ext}'):
                filename1 += f'.{format_ext}'
            if not filename2.lower().endswith(f'.{format_ext}'):
                filename2 += f'.{format_ext}'
                
            # Create full paths
            output1 = os.path.join(save_dir, filename1)
            output2 = os.path.join(save_dir, filename2)
            
            # Update progress
            self.status_label.configure(
                text=f"Création des {format_type} 300 DPI...",
                text_color=("blue", "lightblue")
            )
            self.root.update()
            
            # Export based on format
            if format_type == "PDF":
                # Save as PDF with high quality (300 DPI resolution preserved)
                self.combined_image1.save(output1, 'PDF', 
                                        quality=100, 
                                        resolution=300.0)
                self.combined_image2.save(output2, 'PDF', 
                                        quality=100, 
                                        resolution=300.0)
                
                # Update status
                self.status_label.configure(
                    text="PDF 300 DPI exportés avec succès !",
                    text_color=("green", "lightgreen")
                )
                
                # Show custom success popup
                self.show_success_popup("PDF", filename1, filename2, save_dir, 
                                      "Format: PDF vectoriel\nDimensions originales préservées")
                
            else:  # PNG
                # Save as PNG with high quality (300 DPI resolution preserved)
                self.combined_image1.save(output1, 'PNG', 
                                        quality=100, 
                                        dpi=(300, 300))
                self.combined_image2.save(output2, 'PNG', 
                                        quality=100, 
                                        dpi=(300, 300))
                
                # Update status
                self.status_label.configure(
                    text="PNG 300 DPI exportés avec succès !",
                    text_color=("green", "lightgreen")
                )
                
                # Show custom success popup
                self.show_success_popup("PNG", filename1, filename2, save_dir, 
                                      "Format: PNG haute résolution\nDimensions: Qualité professionnelle")
                              
        except Exception as e:
            self.status_label.configure(
                text=f"✗ Erreur lors de l'export: {str(e)}",
                text_color=("red", "lightcoral")
            )
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")
            
    def show_success_popup(self, format_type, filename1, filename2, save_dir, format_info):
        """Show custom success popup window"""
        # Create popup window
        popup = ctk.CTkToplevel(self.root)
        popup.title("Export Réussi")
        popup.geometry("500x400")
        popup.resizable(False, False)
        
        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        
        # Header
        header_frame = ctk.CTkFrame(popup, corner_radius=0, height=80, fg_color=("green", "darkgreen"))
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        success_icon = ctk.CTkLabel(
            header_frame,
            text="✓",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="white"
        )
        success_icon.pack(pady=20)
        
        # Main content
        content_frame = ctk.CTkFrame(popup, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text=f"Export {format_type} Terminé !",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("green", "lightgreen")
        )
        title_label.pack(pady=(0, 20))
        
        # Files info
        files_frame = ctk.CTkFrame(content_frame, corner_radius=8)
        files_frame.pack(fill="x", pady=10)
        
        files_title = ctk.CTkLabel(
            files_frame,
            text="Fichiers créés:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        files_title.pack(pady=(15, 5))
        
        file1_label = ctk.CTkLabel(
            files_frame,
            text=f"• {filename1}",
            font=ctk.CTkFont(size=12)
        )
        file1_label.pack(pady=2)
        
        file2_label = ctk.CTkLabel(
            files_frame,
            text=f"• {filename2}",
            font=ctk.CTkFont(size=12)
        )
        file2_label.pack(pady=(2, 15))
        
        # Quality info
        quality_frame = ctk.CTkFrame(content_frame, corner_radius=8)
        quality_frame.pack(fill="x", pady=10)
        
        quality_label = ctk.CTkLabel(
            quality_frame,
            text=f"Qualité: 300 DPI (professionnelle)\n{format_info}",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        quality_label.pack(pady=15)
        
        # Location info
        location_frame = ctk.CTkFrame(content_frame, corner_radius=8)
        location_frame.pack(fill="x", pady=10)
        
        location_title = ctk.CTkLabel(
            location_frame,
            text="Emplacement:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        location_title.pack(pady=(10, 5))
        
        location_label = ctk.CTkLabel(
            location_frame,
            text=save_dir,
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray40")
        )
        location_label.pack(pady=(0, 10))
        
        # Buttons
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        open_folder_btn = ctk.CTkButton(
            buttons_frame,
            text="Ouvrir Dossier",
            command=lambda: self.open_folder(save_dir),
            width=150,
            height=35,
            corner_radius=6
        )
        open_folder_btn.pack(side="left", padx=(0, 10))
        
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Fermer",
            command=popup.destroy,
            width=100,
            height=35,
            corner_radius=6,
            fg_color=("green", "darkgreen"),
            hover_color=("lightgreen", "green")
        )
        close_btn.pack(side="right")
        
    def open_folder(self, folder_path):
        """Open folder in file explorer"""
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                subprocess.run(['explorer', folder_path])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', folder_path])
            else:  # Linux
                subprocess.run(['xdg-open', folder_path])
        except Exception as e:
            print(f"Could not open folder: {e}")


def main():
    root = ctk.CTk()
    app = ModernPDFCombinerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 