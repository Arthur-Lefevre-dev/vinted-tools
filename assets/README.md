# Assets - Icônes et Ressources

## 📁 Structure

```
assets/
├── icon.ico          # Icône de l'application (recommandé)
├── icon.png          # Version PNG de l'icône (optionnel)
└── README.md         # Ce fichier
```

## 🖼️ Icônes Supportées

### Pour l'Application Windows

- **Nom du fichier** : `icon.ico`
- **Format** : ICO (Windows Icon)
- **Tailles recommandées** : 16x16, 32x32, 48x48, 64x64, 128x128, 256x256 pixels
- **Utilisation** : Icône de la fenêtre et de l'exécutable

### Pour l'Exécutable Compilé

- **Nom du fichier** : `icon.ico`
- **Format** : ICO uniquement
- **Taille recommandée** : 256x256 pixels minimum
- **Utilisation** : Icône de l'exécutable .exe

## 🎨 Comment Créer/Ajouter une Icône

### Méthode 1 : Icône Existante

1. Trouvez une icône au format `.ico`
2. Nommez-la `icon.ico`
3. Placez-la dans le dossier `assets/`

### Méthode 2 : Convertir PNG/JPG vers ICO

```bash
# Avec ImageMagick
convert mon_logo.png -resize 256x256 assets/icon.ico

# Avec des sites en ligne
# https://convertio.co/png-ico/
# https://www.icoconverter.com/
```

### Méthode 3 : Créer avec des Outils

- **GIMP** (gratuit) : Exporter en .ico
- **Paint.NET** : Plugin ICO
- **Adobe Photoshop** : Plugin ICO
- **Online-Convert.com** : Convertisseur en ligne

## 🔧 Configuration

### Titre de l'Application

Modifiez dans `src/config.py` :

```python
WINDOW_TITLE: str = "Mon Super PDF Tool"  # 👈 Votre titre ici
```

### Chemin de l'Icône

Modifiez dans `src/config.py` :

```python
WINDOW_ICON: str = "assets/icon.ico"  # 👈 Chemin vers votre icône
```

## ✅ Vérification

### Test de l'Icône

1. Placez votre `icon.ico` dans `assets/`
2. Lancez l'application : `python main.py`
3. Vérifiez que l'icône apparaît dans :
   - La barre de titre de la fenêtre
   - La barre des tâches Windows

### Test de l'Exécutable

1. Compilez : `build_exe.bat`
2. Vérifiez l'icône dans :
   - Le fichier `dist/PDF_Combiner.exe`
   - L'explorateur Windows
   - La barre des tâches lors de l'exécution

## 📏 Spécifications Techniques

### Format ICO Optimal

```
Tailles multiples dans un seul fichier .ico :
- 16x16 (icône système)
- 32x32 (icône par défaut)
- 48x48 (grande icône)
- 64x64 (icône HD)
- 128x128 (très grande icône)
- 256x256 (icône haute résolution)
```

### Compatibilité

- **Windows** : .ico (recommandé)
- **Application Python** : .ico, .png, .gif
- **Exécutable PyInstaller** : .ico uniquement

## 🚨 Dépannage

### L'icône ne s'affiche pas

1. Vérifiez le chemin dans `config.py`
2. Vérifiez que le fichier existe : `assets/icon.ico`
3. Vérifiez le format (doit être .ico pour Windows)
4. Relancez l'application

### L'icône de l'exe est incorrecte

1. Vérifiez que `assets/icon.ico` existe avant compilation
2. Recompilez avec `build_exe.bat`
3. Vérifiez dans `dist/PDF_Combiner.exe`

### Icône de mauvaise qualité

- Utilisez une résolution minimum de 256x256
- Assurez-vous que l'image source est nette
- Créez un fichier .ico multi-résolutions

---

**Note** : Si aucune icône n'est fournie, l'application utilisera l'icône par défaut de Python/Tkinter.
