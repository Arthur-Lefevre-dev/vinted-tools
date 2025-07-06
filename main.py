"""
Main entry point for PDF Combiner application
"""

import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from pdf2image import convert_from_path
except ImportError:
    print("pdf2image n'est pas installé. Veuillez installer les dépendances avec: pip install -r requirements.txt")
    sys.exit(1)

from src.controller import AppController
from src.exceptions import PDFCombinerError


def main():
    """Main application entry point"""
    try:
        # Create and run application
        app = AppController()
        app.run()
    except PDFCombinerError as e:
        print(f"Erreur de l'application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\\nApplication interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 