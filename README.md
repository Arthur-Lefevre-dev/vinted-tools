# PDF Combiner 2.0

> **Combinateur PDF Professionnel** - Une application moderne pour combiner les moitiés de deux PDF A4 avec une interface intuitive.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Fonctionnalités

- 🔄 **Combinaison intelligente** : Combine automatiquement les moitiés de deux PDF
- 🖼️ **Aperçu en temps réel** : Visualisez le résultat avant l'export
- 📄 **Pages blanches** : Ajoutez des pages blanches si nécessaire
- 🔄 **Orientation** : Support portrait et paysage
- 📤 **Multi-format** : Export en PDF ou PNG haute qualité (300 DPI)
- 🎨 **Interface moderne** : Design professionnel avec CustomTkinter
- ⚡ **Performance** : Traitement en arrière-plan avec barre de progression

## 🚀 Installation et Utilisation

### Option 1 : Exécutable Standalone (Recommandé)

**Téléchargez et utilisez directement - aucune installation requise !**

1. **Compilez l'exécutable** :

   ```bash
   # Méthode automatique
   build_exe.bat

   # Ou méthode rapide
   quick_build.bat
   ```

2. **Lancez l'application** :
   - Double-cliquez sur `dist/PDF_Combiner.exe`
   - Ou utilisez `test_exe.bat` pour tester

### Option 2 : Exécution avec Python

1. **Installation des dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

2. **Lancement** :
   ```bash
   python main.py
   # Ou double-cliquez sur start.bat
   ```

## 🏗️ Architecture

Cette application utilise une **architecture modulaire moderne** :

```
src/
├── models/          # Modèles de données
├── core/            # Logique métier
├── ui/              # Interface utilisateur
├── controller/      # Contrôleur principal
├── utils/           # Utilitaires
├── config.py        # Configuration
└── exceptions.py    # Gestion d'erreurs
```

**Avantages** :

- ✅ Code maintenable et extensible
- ✅ Séparation des responsabilités
- ✅ Facile à tester et déboguer
- ✅ Architecture professionnelle

## 🔧 Compilation en Exécutable

### Compilation Rapide

```bash
# Tout automatique
build_exe.bat

# Compilation simple
quick_build.bat

# Nettoyage
clean_build.bat
```

### Options Avancées

```python
# Personnalisez dans build_exe.py
- Ajout d'icône
- Optimisation de taille
- Mode debug
- Exclusion de modules
```

Consultez [BUILD_GUIDE.md](BUILD_GUIDE.md) pour plus de détails.

## 📋 Prérequis Système

### Pour la Compilation

- **Python 3.8+**
- **Windows 10/11** (pour .exe)
- **4 Go RAM** minimum
- **500 Mo d'espace libre**

### Pour l'Exécutable

- **Windows 10/11**
- **Microsoft Visual C++ Redistributable** (généralement préinstallé)
- **100 Mo d'espace libre**

## 💡 Utilisation

1. **Sélectionnez vos PDF** ou utilisez des pages blanches
2. **Choisissez l'orientation** (Portrait/Paysage)
3. **Cliquez sur "Combiner"** pour traiter
4. **Prévisualisez** le résultat
5. **Exportez** en PDF ou PNG haute qualité

### Résultat

- **Fichier 1** : Toutes les moitiés hautes combinées
- **Fichier 2** : Toutes les moitiés basses combinées

## 🛠️ Scripts Utiles

| Script            | Description                             |
| ----------------- | --------------------------------------- |
| `start.bat`       | Lance l'application Python              |
| `build_exe.bat`   | Compilation complète avec vérifications |
| `quick_build.bat` | Compilation rapide                      |
| `test_exe.bat`    | Test de l'exécutable                    |
| `clean_build.bat` | Nettoyage des fichiers de build         |

## 📊 Spécifications Techniques

- **Résolution** : 300 DPI (qualité professionnelle)
- **Formats supportés** : PDF, PNG
- **Taille exe** : ~80-120 MB
- **Temps de démarrage** : 3-8 secondes
- **RAM utilisée** : 50-100 MB

## 🔍 Dépannage

### Problèmes Courants

1. **"pdf2image n'est pas installé"**

   ```bash
   pip install -r requirements.txt
   ```

2. **Compilation échoue**

   ```bash
   clean_build.bat
   pip install --upgrade pip setuptools
   build_exe.bat
   ```

3. **Executable ne démarre pas**
   - Vérifiez l'antivirus
   - Testez sur machine propre
   - Consultez [BUILD_GUIDE.md](BUILD_GUIDE.md)

## 📁 Structure des Fichiers

```
├── src/                    # Code source modulaire
├── main.py                 # Point d'entrée
├── requirements.txt        # Dépendances Python
├── build_exe.py           # Script de compilation
├── build_exe.bat          # Compilation automatique
├── BUILD_GUIDE.md         # Guide de compilation détaillé
├── ARCHITECTURE.md        # Documentation architecture
└── dist/                  # Exécutable compilé (après build)
    └── PDF_Combiner.exe
```

## 🆕 Nouveautés v2.0

- ✨ **Architecture modulaire** complètement refactorisée
- 🚀 **Compilation en exécutable** simplifiée
- 🎨 **Interface améliorée** avec composants modulaires
- 🔧 **Configuration centralisée**
- 🛡️ **Gestion d'erreurs** robuste
- 📝 **Documentation complète**

## 🤝 Contribution

L'architecture modulaire facilite grandement les contributions :

1. **Models** : Ajoutez de nouveaux types de documents
2. **Core** : Étendez les capacités de traitement
3. **UI** : Créez de nouveaux composants
4. **Utils** : Ajoutez des utilitaires

## 📄 License

MIT License - Voir le fichier LICENSE

## 👨‍💻 Auteur

**Dragolelele** - Version 2.0 avec architecture modulaire

---

> 💡 **Astuce** : Utilisez `build_exe.bat` pour créer un exécutable prêt à distribuer sans dépendances Python !
