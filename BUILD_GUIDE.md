# Guide de Compilation - PDF Combiner

## 🚀 Compilation Rapide

### Méthode 1 : Script automatique (Recommandé)

```bash
# Double-cliquez sur le fichier ou lancez en ligne de commande
build_exe.bat
```

### Méthode 2 : Commande Python directe

```bash
python build_exe.py
```

### Méthode 3 : PyInstaller direct (Avancé)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name PDF_Combiner main.py
```

## 📋 Prérequis

1. **Python 3.8+** installé sur votre système
2. **Toutes les dépendances** installées :
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Options de Compilation

### Configuration Standard

- **Type** : Exécutable unique (onefile)
- **Interface** : Mode fenêtré (sans console)
- **Nom** : PDF_Combiner.exe
- **Taille** : ~50-100 MB

### Configuration Debug

Pour déboguer les erreurs, modifiez dans `build_exe.py` :

```python
console=True,  # Affiche la console pour voir les erreurs
debug=True,    # Mode debug activé
```

## 📁 Fichiers Générés

Après compilation, vous obtiendrez :

```
dist/
└── PDF_Combiner.exe    # Exécutable final

build/                  # Fichiers temporaires (peut être supprimé)
pdf_combiner.spec      # Configuration PyInstaller (généré automatiquement)
EXECUTABLE_INFO.md     # Information sur l'exécutable
```

## 🎯 Optimisations

### Réduction de Taille

Pour réduire la taille de l'exécutable :

1. **Excluez les modules inutiles** dans le fichier spec :

   ```python
   excludes=['matplotlib', 'numpy', 'pandas', ...]
   ```

2. **Utilisez UPX** (compression) :

   ```python
   upx=True,
   ```

3. **Compilation séparée** (plusieurs fichiers) :
   ```bash
   pyinstaller --onedir main.py
   ```

### Amélioration des Performances

- **Cache des imports** : PyInstaller met en cache automatiquement
- **Optimisation Python** : Utilisez `python -O` pour la compilation

## 🖼️ Ajouter une Icône

1. Placez votre fichier `.ico` dans le projet
2. Modifiez dans `build_exe.py` :
   ```python
   icon='mon_icone.ico',
   ```

## 🔍 Dépannage

### Erreurs Communes

#### "Module not found"

```bash
# Ajoutez le module dans hiddenimports
hiddenimports=['module_manquant']
```

#### "Failed to execute script"

```bash
# Activez le mode console pour voir l'erreur
console=True
```

#### "Permission denied"

```bash
# Exécutez en tant qu'administrateur
# Ou désactivez temporairement l'antivirus
```

#### "DLL load failed"

```bash
# Réinstallez les dépendances
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

### Tests de l'Exécutable

1. **Test local** : Double-cliquez sur l'exe
2. **Test sur machine propre** : Testez sur un PC sans Python
3. **Test antivirus** : Vérifiez que l'antivirus ne bloque pas

## 📦 Distribution

### Fichiers à Distribuer

- `PDF_Combiner.exe` (obligatoire)
- Documentation utilisateur (optionnel)

### Méthodes de Distribution

1. **Envoi direct** : Envoyez juste l'exe
2. **Archive ZIP** : Compressez avec documentation
3. **Installateur** : Utilisez NSIS ou Inno Setup pour un vrai installateur

## 🧹 Nettoyage

Pour nettoyer les fichiers de compilation :

```bash
# Automatique
clean_build.bat

# Manuel
rmdir /s build dist
del pdf_combiner.spec
```

## ⚡ Compilation en Une Commande

```bash
# Installation + Compilation + Test
pip install -r requirements.txt && python build_exe.py && dist\PDF_Combiner.exe
```

## 📊 Statistiques Typiques

- **Temps de compilation** : 2-5 minutes
- **Taille exe** : 80-120 MB
- **Temps de démarrage** : 3-8 secondes
- **RAM utilisée** : 50-100 MB

## 🆘 Support

En cas de problème :

1. Vérifiez les dépendances avec `pip list`
2. Testez d'abord avec `python main.py`
3. Activez le mode debug dans la compilation
4. Consultez les logs PyInstaller dans `build/`

---

**Note** : L'exécutable généré est autonome et ne nécessite pas Python sur la machine cible.
