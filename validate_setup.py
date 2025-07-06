#!/usr/bin/env python3
"""
Script de validation pour PDF Combiner
Vérifie que tout est prêt avant la compilation
"""

import os
import sys
from pathlib import Path


def check_file_exists(file_path: str, description: str) -> bool:
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - MANQUANT")
        return False


def check_directory_exists(dir_path: str, description: str) -> bool:
    """Check if a directory exists"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} - MANQUANT")
        return False


def check_icon_file():
    """Check icon file specifically"""
    icon_path = "assets/icon.ico"
    if os.path.exists(icon_path):
        file_size = os.path.getsize(icon_path)
        print(f"✅ Icône trouvée: {icon_path} ({file_size} bytes)")
        
        # Check if it's a valid ICO file
        with open(icon_path, 'rb') as f:
            header = f.read(4)
            if header[:2] == b'\x00\x00' and header[2:4] == b'\x01\x00':
                print("✅ Format ICO valide")
                return True
            else:
                print("❌ Format ICO invalide")
                return False
    else:
        print(f"❌ Icône manquante: {icon_path}")
        print("💡 Créez ou copiez votre icône dans le dossier assets/")
        return False


def check_python_modules():
    """Check required Python modules"""
    required_modules = [
        'pdf2image',
        'PIL',
        'customtkinter',
        'tkinter'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Module {module} installé")
        except ImportError:
            print(f"❌ Module {module} manquant")
            missing_modules.append(module)
    
    return len(missing_modules) == 0


def test_imports():
    """Test application imports"""
    sys.path.insert(0, 'src')
    
    imports_to_test = [
        ('src.config', 'config'),
        ('src.exceptions', 'PDFCombinerError'),
        ('src.models', 'PDFDocument'),
        ('src.core', 'PDFProcessor'),
        ('src.utils', 'validate_pdf_file'),
        ('src.ui', 'MainWindow'),
        ('src.controller', 'AppController'),
    ]
    
    failed_imports = []
    for module_name, item_name in imports_to_test:
        try:
            module = __import__(module_name, fromlist=[item_name])
            getattr(module, item_name)
            print(f"✅ Import {module_name}.{item_name} réussi")
        except ImportError as e:
            print(f"❌ Import {module_name}.{item_name} échoué: {e}")
            failed_imports.append(f"{module_name}.{item_name}")
        except AttributeError as e:
            print(f"❌ Attribut {module_name}.{item_name} manquant: {e}")
            failed_imports.append(f"{module_name}.{item_name}")
    
    return len(failed_imports) == 0


def main():
    """Main validation function"""
    print("="*60)
    print("🔍 VALIDATION - PDF Combiner")
    print("="*60)
    
    all_good = True
    
    # Check core files
    print("\n📁 Fichiers principaux:")
    all_good &= check_file_exists("main.py", "Point d'entrée")
    all_good &= check_file_exists("build_exe.py", "Script de compilation")
    all_good &= check_file_exists("requirements.txt", "Dépendances")
    
    # Check source directory
    print("\n📂 Structure du projet:")
    all_good &= check_directory_exists("src", "Dossier source")
    all_good &= check_directory_exists("src/core", "Dossier core")
    all_good &= check_directory_exists("src/ui", "Dossier UI")
    all_good &= check_directory_exists("src/controller", "Dossier controller")
    all_good &= check_directory_exists("src/models", "Dossier models")
    all_good &= check_directory_exists("src/utils", "Dossier utils")
    all_good &= check_directory_exists("assets", "Dossier assets")
    
    # Check key source files
    print("\n🐍 Fichiers source:")
    all_good &= check_file_exists("src/core/pdf_processor.py", "Processeur PDF")
    all_good &= check_file_exists("src/ui/main_window.py", "Fenêtre principale")
    all_good &= check_file_exists("src/controller/app_controller.py", "Contrôleur")
    all_good &= check_file_exists("src/config.py", "Configuration")
    all_good &= check_file_exists("src/exceptions.py", "Exceptions")
    all_good &= check_file_exists("src/models/__init__.py", "Modèles")
    
    # Check icon
    print("\n🖼️ Icône:")
    all_good &= check_icon_file()
    
    # Check Python modules
    print("\n📦 Modules Python:")
    all_good &= check_python_modules()
    
    # Test imports
    print("\n🧪 Test des imports:")
    all_good &= test_imports()
    
    # Check configuration
    print("\n⚙️ Configuration:")
    try:
        sys.path.insert(0, 'src')
        from config import config
        print(f"✅ Titre: {config.WINDOW_TITLE}")
        print(f"✅ Icône: {config.WINDOW_ICON}")
        print(f"✅ Taille: {config.WINDOW_SIZE}")
        print(f"✅ DPI Export: {config.EXPORT_DPI}")
    except ImportError as e:
        print(f"❌ Impossible d'importer la configuration: {e}")
        all_good = False
    except AttributeError as e:
        print(f"❌ Attribut manquant dans la configuration: {e}")
        all_good = False
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        all_good = False
    
    # Results
    print("\n" + "="*60)
    if all_good:
        print("🎉 VALIDATION RÉUSSIE!")
        print("✅ Prêt pour la compilation avec build_exe.bat")
        print("✅ Prêt pour le test avec test_fixes.bat")
    else:
        print("❌ VALIDATION ÉCHOUÉE!")
        print("⚠️  Corrigez les erreurs ci-dessus avant de continuer")
    
    print("="*60)
    
    # Recommendations
    if not all_good:
        print("\n💡 RECOMMANDATIONS:")
        print("1. Vérifiez que tous les fichiers sont présents")
        print("2. Installez les dépendances: pip install -r requirements.txt")
        print("3. Ajoutez votre icône dans assets/icon.ico")
        print("4. Relancez ce script de validation")
    
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main()) 