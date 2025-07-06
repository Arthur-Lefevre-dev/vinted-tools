@echo off
echo Compilation rapide en cours...
pip install -q pyinstaller
pyinstaller --onefile --windowed --name PDF_Combiner --clean main.py
if exist "dist\PDF_Combiner.exe" (
    echo SUCCESS! Executable cree: dist\PDF_Combiner.exe
    start "" "dist\"
) else (
    echo ERREUR: Compilation echouee
)
pause 