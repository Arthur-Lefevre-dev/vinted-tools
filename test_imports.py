#!/usr/bin/env python3
"""
Test rapide des imports principaux
"""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test all main imports"""
    print("🧪 Test des imports principaux...")
    
    errors = []
    
    # Test config
    try:
        from src.config import config
        print("✅ Config importé")
    except Exception as e:
        errors.append(f"Config: {e}")
        print(f"❌ Config: {e}")
    
    # Test exceptions
    try:
        from src.exceptions import PDFCombinerError
        print("✅ Exceptions importées")
    except Exception as e:
        errors.append(f"Exceptions: {e}")
        print(f"❌ Exceptions: {e}")
    
    # Test models
    try:
        from src.models import PDFDocument, CombinedDocument
        print("✅ Models importés")
    except Exception as e:
        errors.append(f"Models: {e}")
        print(f"❌ Models: {e}")
    
    # Test core
    try:
        from src.core import PDFProcessor
        print("✅ Core importé")
    except Exception as e:
        errors.append(f"Core: {e}")
        print(f"❌ Core: {e}")
    
    # Test utils
    try:
        from src.utils import validate_pdf_file
        print("✅ Utils importés")
    except Exception as e:
        errors.append(f"Utils: {e}")
        print(f"❌ Utils: {e}")
    
    # Test UI
    try:
        from src.ui import MainWindow
        print("✅ UI importé")
    except Exception as e:
        errors.append(f"UI: {e}")
        print(f"❌ UI: {e}")
    
    # Test controller
    try:
        from src.controller import AppController
        print("✅ Controller importé")
    except Exception as e:
        errors.append(f"Controller: {e}")
        print(f"❌ Controller: {e}")
    
    # Test external dependencies
    try:
        import pdf2image
        print("✅ pdf2image importé")
    except Exception as e:
        errors.append(f"pdf2image: {e}")
        print(f"❌ pdf2image: {e}")
    
    try:
        import customtkinter
        print("✅ customtkinter importé")
    except Exception as e:
        errors.append(f"customtkinter: {e}")
        print(f"❌ customtkinter: {e}")
    
    try:
        from PIL import Image
        print("✅ PIL importé")
    except Exception as e:
        errors.append(f"PIL: {e}")
        print(f"❌ PIL: {e}")
    
    print("\n" + "="*50)
    if errors:
        print("❌ ERREURS DÉTECTÉES:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ TOUS LES IMPORTS FONCTIONNENT!")
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 