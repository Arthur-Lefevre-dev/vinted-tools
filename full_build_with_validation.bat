@echo off
setlocal enabledelayedexpansion

echo ========================================
echo BUILD COMPLET - PDF Combiner
echo ========================================

echo.
echo 1. Validation de la configuration...
echo.

python validate_setup.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Validation échouée! Corrigez les erreurs ci-dessus.
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Validation réussie!
echo.

echo 2. Nettoyage des builds précédents...
echo.
call clean_build.bat

echo.
echo 3. Compilation avec icône...
echo.
call build_exe.bat
if %errorlevel% neq 0 (
    echo.
    echo ❌ Compilation échouée!
    pause
    exit /b 1
)

echo.
echo ✅ Compilation réussie!
echo.

echo 4. Vérification de l'exécutable...
echo.
if exist "dist\PDF_Combiner.exe" (
    echo ✅ Exécutable créé: dist\PDF_Combiner.exe
    
    REM Afficher la taille du fichier
    for %%I in ("dist\PDF_Combiner.exe") do (
        set /a size_mb=%%~zI/1024/1024
        echo ℹ️  Taille: !size_mb! MB
    )
    
    echo.
    echo 5. Test rapide de l'exécutable...
    echo.
    echo Lancement de l'exécutable pour test...
    echo (L'application va s'ouvrir - fermez-la pour continuer)
    echo.
    
    start /wait "" "dist\PDF_Combiner.exe"
    
    echo.
    echo ✅ Test terminé!
    
) else (
    echo ❌ Exécutable non trouvé dans dist\
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 BUILD COMPLET TERMINÉ AVEC SUCCÈS!
echo ========================================
echo.
echo 📁 Fichiers créés:
echo   - dist\PDF_Combiner.exe
echo   - build\ (dossier temporaire)
echo   - pdf_combiner.spec
echo.
echo 🔍 Vérifications manuelles:
echo   ✅ Icône dans la barre de titre
echo   ✅ Icône dans la barre des tâches
echo   ✅ Pas de fenêtres cmd lors du traitement
echo   ✅ Pas de freeze pendant le traitement
echo.
echo 🚀 Prêt pour la distribution!
echo.
pause 