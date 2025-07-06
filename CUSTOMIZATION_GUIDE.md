# Guide de Personnalisation - PDF Combiner

## 🎨 Changer le Titre de l'Application

### 1. **Configuration Centralisée**

Modifiez le titre dans `src/config.py` :

```python
# Window settings
WINDOW_TITLE: str = "Mon Super PDF Tool"  # 👈 Changez ici
```

**Résultat :**

- ✅ Titre de la fenêtre
- ✅ Titre dans l'en-tête de l'interface
- ✅ Nom de l'exécutable

### 2. **Titre du Sous-titre** (Optionnel)

Modifiez dans `src/ui/main_window.py`, ligne ~77 :

```python
subtitle_label = ctk.CTkLabel(
    header_frame,
    text="Mon slogan personnalisé • Export professionnel",  # 👈 Changez ici
    font=ctk.CTkFont(size=13),
    text_color=("gray60", "gray40")
)
```

## 🖼️ Ajouter une Icône Personnalisée

### 1. **Préparez votre Icône**

#### Format Requis

- **Format** : `.ico` (Windows Icon)
- **Taille** : 256x256 pixels minimum
- **Multi-résolutions** : 16x16, 32x32, 48x48, 64x64, 128x128, 256x256

#### Convertir PNG/JPG vers ICO

```bash
# Avec ImageMagick
convert mon_logo.png -resize 256x256 assets/icon.ico

# Sites en ligne recommandés :
# https://convertio.co/png-ico/
# https://www.icoconverter.com/
```

### 2. **Placez l'Icône**

```
assets/
└── icon.ico  # 👈 Votre icône ici
```

### 3. **Configuration Automatique**

L'icône sera automatiquement détectée si elle est dans `assets/icon.ico`.

**Pour un chemin personnalisé**, modifiez `src/config.py` :

```python
WINDOW_ICON: str = "mon_dossier/mon_icone.ico"  # 👈 Chemin personnalisé
```

### 4. **Test**

```bash
# Test de l'application
python main.py

# Test de l'exécutable
build_exe.bat
```

## 🎨 Personnaliser l'Interface

### 1. **Couleurs et Thème**

Modifiez dans `src/config.py` :

```python
# Theme settings
APPEARANCE_MODE: str = "dark"    # "dark", "light", "system"
COLOR_THEME: str = "blue"        # "blue", "green", "dark-blue"
```

### 2. **Taille de Fenêtre**

```python
# Window settings
WINDOW_SIZE: Tuple[int, int] = (1400, 1000)  # 👈 Largeur x Hauteur
```

### 3. **Qualité d'Export**

```python
# Image processing settings
EXPORT_DPI: int = 400           # 👈 300 DPI par défaut, augmentez pour plus de qualité
EXPORT_QUALITY: int = 100       # 👈 Qualité JPEG/PNG (0-100)
```

### 4. **Formats Supportés**

```python
# Export settings
SUPPORTED_FORMATS: Tuple[str, ...] = ("PDF", "PNG", "JPEG")  # 👈 Ajoutez d'autres formats
```

## 🚀 Personnaliser l'Exécutable

### 1. **Nom de l'Exécutable**

Modifiez dans `build_exe.py`, ligne ~98 :

```python
name='Mon_PDF_Tool',  # 👈 Nom du fichier .exe
```

### 2. **Icône de l'Exécutable**

L'icône est automatiquement incluse si `assets/icon.ico` existe.

### 3. **Métadonnées de l'Exécutable**

Ajoutez dans le fichier spec généré :

```python
exe = EXE(
    # ... autres paramètres ...
    version='version_info.txt',  # 👈 Fichier de version
    company_name='Mon Entreprise',
    file_description='Mon Combinateur PDF',
    copyright='© 2024 Mon Nom',
)
```

## 📝 Personnaliser les Messages

### 1. **Messages d'Interface**

Modifiez dans les composants UI (`src/ui/components/`) :

```python
# Exemple dans pdf_selection_panel.py
text="Sélectionner mes documents"  # 👈 Au lieu de "Sélectionner les PDF"
```

### 2. **Messages d'Erreur**

Modifiez dans `src/exceptions.py` ou directement dans le code :

```python
raise PDFLoadError("Impossible de charger votre document")  # 👈 Messages personnalisés
```

### 3. **Noms de Fichiers par Défaut**

Modifiez dans `src/config.py` :

```python
# Default filenames
DEFAULT_TOP_FILENAME: str = "document_haut"      # 👈 Nom par défaut
DEFAULT_BOTTOM_FILENAME: str = "document_bas"    # 👈 Nom par défaut
```

## 🔧 Personnalisations Avancées

### 1. **Nouveau Format d'Export**

Ajoutez dans `src/utils/image_utils.py` :

```python
def save_image_with_format(image, file_path, format_type, quality=100, dpi=300):
    if format_type.upper() == "JPEG":  # 👈 Nouveau format
        image.save(file_path, 'JPEG', quality=quality, dpi=(dpi, dpi))
    # ... autres formats ...
```

### 2. **Nouveau Composant UI**

Créez dans `src/ui/components/mon_composant.py` :

```python
class MonComposant(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # Votre composant personnalisé
```

### 3. **Nouvelle Fonctionnalité**

Étendez `src/core/pdf_processor.py` :

```python
def ma_nouvelle_fonction(self):
    # Votre logique métier
    pass
```

## ✅ Liste de Vérification

### Avant Compilation

- [ ] Titre modifié dans `config.py`
- [ ] Icône placée dans `assets/icon.ico`
- [ ] Application testée avec `python main.py`
- [ ] Icône visible dans la fenêtre et barre des tâches

### Après Compilation

- [ ] Exécutable généré dans `dist/`
- [ ] Icône visible sur le fichier .exe
- [ ] Titre correct dans l'explorateur Windows
- [ ] Application fonctionne sans Python

### Test Final

- [ ] Test sur machine sans Python installé
- [ ] Vérification des permissions
- [ ] Test antivirus (faux positifs possibles)

## 🎨 Exemples de Personnalisation

### Exemple 1 : Application Médicale

```python
WINDOW_TITLE: str = "MedDoc Combiner"
# Icône : stéthoscope ou croix médicale
# Couleurs : blanc/bleu médical
```

### Exemple 2 : Application Juridique

```python
WINDOW_TITLE: str = "LegalDoc Pro"
# Icône : balance de justice ou document légal
# Couleurs : noir/or professionnel
```

### Exemple 3 : Application Éducative

```python
WINDOW_TITLE: str = "EduPDF Tools"
# Icône : livre ou graduation cap
# Couleurs : vert/orange éducatif
```

## 🆘 Dépannage

### L'icône ne s'affiche pas

1. Vérifiez le format (.ico requis)
2. Vérifiez le chemin dans `config.py`
3. Redémarrez l'application

### Le titre ne change pas

1. Vérifiez `src/config.py`
2. Redémarrez l'application
3. Recompilez si nécessaire

### L'exécutable a l'ancienne icône

1. Vérifiez que `assets/icon.ico` existe
2. Recompilez avec `build_exe.bat`
3. Supprimez le cache : `clean_build.bat`

---

**💡 Astuce** : Gardez une sauvegarde de vos personnalisations avant de mettre à jour le code source !
