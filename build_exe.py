#!/usr/bin/env python3
"""
Script to build PDF Combiner application as standalone executable
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path


def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))


def check_dependencies():
    """Check if all required dependencies are installed"""
    # Map package names to their import names
    packages_map = {
        'pyinstaller': 'PyInstaller',
        'pdf2image': 'pdf2image',
        'customtkinter': 'customtkinter',
        'Pillow': 'PIL'
    }
    
    missing_packages = []
    for package_name, import_name in packages_map.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name} is installed")
        except ImportError:
            missing_packages.append(package_name)
            print(f"❌ {package_name} not found")
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install with: pip install -r requirements.txt")
        return False
    
    return True


def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Analysis
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/icon.ico', 'assets'),
    ] if os.path.exists('assets/icon.ico') else [],
    hiddenimports=[
        'pdf2image',
        'PIL',
        'PIL._tkinter_finder',
        'customtkinter',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'packaging.version',
        'packaging.specifiers',
        'packaging.requirements',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'torch',
        'tensorflow',
        'jupyter',
        'notebook',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF_Combiner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
         entitlements_file=None,
     icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,  # Auto-detect icon
)
"""
    
    with open('pdf_combiner.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✓ Created pdf_combiner.spec")


def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    try:
        # Run PyInstaller with spec file
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'pdf_combiner.spec'
        ], check=True, capture_output=True, text=True)
        
        print("✓ Build successful!")
        print(f"Executable created: {Path('dist/PDF_Combiner.exe').absolute()}")
        
        # Show file size
        exe_path = Path('dist/PDF_Combiner.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"File size: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed!")
        print(f"Error: {e.stderr}")
        return False


def create_installer_info():
    """Create installer information file"""
    info_content = """# PDF Combiner - Exécutable Standalone

## Utilisation

L'exécutable `PDF_Combiner.exe` est maintenant prêt à être distribué.

### Fichiers générés :
- `dist/PDF_Combiner.exe` - Exécutable principal
- `build/` - Fichiers de build temporaires (peut être supprimé)

### Distribution :
- L'exécutable est autonome et ne nécessite pas d'installation Python
- Taille approximative : ~50-100 MB (selon les dépendances)
- Compatible avec Windows 10/11

### Dépendances système requises :
- Microsoft Visual C++ Redistributable (généralement déjà installé)
- Pour pdf2image : poppler-utils (inclus dans l'exécutable)

### Test :
Double-cliquez sur `PDF_Combiner.exe` pour lancer l'application.

### Dépannage :
- Si l'application ne démarre pas, lancez depuis cmd pour voir les erreurs
- Vérifiez les permissions d'exécution
- Assurez-vous que l'antivirus n'a pas bloqué le fichier
"""
    
    with open('EXECUTABLE_INFO.md', 'w', encoding='utf-8') as f:
        f.write(info_content)
    
    print("✓ Created EXECUTABLE_INFO.md")


def main():
    """Main build process"""
    print("=" * 60)
    print("PDF Combiner - Build Script")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if not build_executable():
        return 1
    
    # Create info file
    create_installer_info()
    
    print("\n" + "=" * 60)
    print("✅ Build completed successfully!")
    print("=" * 60)
    print(f"Executable location: {Path('dist/PDF_Combiner.exe').absolute()}")
    print("Ready for distribution!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 