@echo off
echo Nettoyage des fichiers de build...

if exist "build" (
    echo Suppression du dossier build...
    rmdir /s /q build
)

if exist "dist" (
    echo Suppression du dossier dist...
    rmdir /s /q dist
)

if exist "pdf_combiner.spec" (
    echo Suppression du fichier spec...
    del pdf_combiner.spec
)

if exist "EXECUTABLE_INFO.md" (
    echo Suppression du fichier info...
    del EXECUTABLE_INFO.md
)

echo Suppression des fichiers .pyc...
for /r %%i in (*.pyc) do del "%%i" 2>nul

echo Suppression des dossiers __pycache__...
for /d /r %%i in (__pycache__) do rmdir /s /q "%%i" 2>nul

echo.
echo Nettoyage termine!
pause 