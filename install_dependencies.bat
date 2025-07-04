@echo off
echo Installation des dependances pour le Combinateur PDF...
echo.
echo Verification de Python...
python --version
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

echo.
echo Installation des packages Python...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERREUR: Echec de l'installation des packages.
    echo.
    echo Solutions possibles:
    echo 1. Verifiez votre connexion internet
    echo 2. Mettez a jour pip: python -m pip install --upgrade pip
    echo 3. Installez les packages separement:
    echo    pip install pdf2image
    echo    pip install Pillow
    echo 4. Si vous avez Python 3.13, essayez:
    echo    pip install pdf2image Pillow --upgrade
    pause
    exit /b 1
)

echo.
echo Installation terminee avec succes!
echo.
echo IMPORTANT: Assurez-vous que Poppler est installe pour pdf2image.
echo Telechargez Poppler depuis: https://github.com/oschwartz10612/poppler-windows/releases/
echo Et ajoutez le dossier 'bin' a votre PATH.
echo.
echo Pour lancer l'application, tapez: python pdf_combiner.py
pause 