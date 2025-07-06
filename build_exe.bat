@echo off
echo ============================================================
echo PDF Combiner - Build to EXE
echo ============================================================
echo.

echo Verification des dependances...
python -c "import sys; print(f'Python version: {sys.version}')"
echo.

echo Installation des dependances si necessaire...
pip install -r requirements.txt
echo.

echo Compilation en cours...
python build_exe.py
echo.

if exist "dist\PDF_Combiner.exe" (
    echo ============================================================
    echo SUCCESS! Executable cree avec succes!
    echo ============================================================
    echo Fichier: dist\PDF_Combiner.exe
    echo.
    echo Voulez-vous tester l'executable? (o/n)
    set /p test="Reponse: "
    if /i "%test%"=="o" (
        echo Lancement de l'executable...
        start "" "dist\PDF_Combiner.exe"
    )
) else (
    echo ============================================================
    echo ERREUR: La compilation a echoue!
    echo ============================================================
    echo Verifiez les erreurs ci-dessus.
)

echo.
echo Appuyez sur une touche pour continuer...
pause >nul 