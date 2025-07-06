@echo off
echo ============================================================
echo Test de l'executable PDF Combiner
echo ============================================================
echo.

if not exist "dist\PDF_Combiner.exe" (
    echo ERREUR: L'executable n'existe pas!
    echo Veuillez d'abord compiler avec build_exe.bat
    echo.
    pause
    exit /b 1
)

echo Informations sur l'executable:
echo.
for %%A in ("dist\PDF_Combiner.exe") do (
    echo Taille: %%~zA octets
    echo Date de creation: %%~tA
)
echo.

echo Lancement de l'executable en mode test...
echo (Fermez l'application pour continuer)
echo.

start /wait "" "dist\PDF_Combiner.exe"

echo.
echo Test termine!
echo.
echo L'application s'est-elle lancee correctement? (o/n)
set /p result="Reponse: "

if /i "%result%"=="o" (
    echo ✓ Test reussi! L'executable fonctionne correctement.
) else (
    echo ✗ Test echoue. Problemes detectes:
    echo   - Verifiez les dependances systeme
    echo   - Testez sur une machine sans Python
    echo   - Consultez BUILD_GUIDE.md pour le depannage
)

echo.
pause 