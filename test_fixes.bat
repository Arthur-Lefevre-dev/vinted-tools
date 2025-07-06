@echo off
echo ========================================
echo Test des Corrections - PDF Combiner
echo ========================================

echo.
echo 1. Test de l'application normale...
echo.
python main.py --test-mode 2>nul
if %errorlevel% neq 0 (
    echo ❌ Erreur lors du test normal
    pause
    exit /b 1
)

echo.
echo 2. Compilation avec icône...
echo.
call build_exe.bat
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de la compilation
    pause
    exit /b 1
)

echo.
echo 3. Vérification de l'icône...
echo.
if exist "dist\PDF_Combiner.exe" (
    echo ✅ Exécutable créé avec succès
    
    REM Vérifier la taille du fichier
    for %%I in ("dist\PDF_Combiner.exe") do (
        set /a size=%%~zI/1024/1024
        echo Taille: !size! MB
    )
    
    echo.
    echo 4. Test de l'exécutable...
    echo.
    echo Lancement de l'exécutable pour test...
    start "" "dist\PDF_Combiner.exe"
    timeout /t 3 /nobreak >nul
    
    echo.
    echo ✅ Test terminé avec succès!
    echo.
    echo Vérifiez que:
    echo - L'icône apparaît dans la barre de titre
    echo - L'icône apparaît dans la barre des tâches
    echo - Aucune fenêtre cmd ne s'ouvre lors du traitement
    echo - L'application ne freeze pas
    
) else (
    echo ❌ Exécutable non trouvé
    pause
    exit /b 1
)

echo.
echo ========================================
echo Test terminé - Vérifiez manuellement
echo ========================================
pause 