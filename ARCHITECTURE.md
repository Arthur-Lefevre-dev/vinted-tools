# Architecture du Combinateur PDF

## Vue d'ensemble

Cette application utilise une architecture modulaire basée sur le pattern MVP (Model-View-Presenter) pour une meilleure maintenabilité et séparation des responsabilités.

## Structure du projet

```
src/
├── __init__.py
├── config.py                    # Configuration centralisée
├── exceptions.py                # Exceptions personnalisées
├── models/                      # Modèles de données
│   ├── __init__.py
│   └── document.py
├── core/                        # Logique métier
│   ├── __init__.py
│   └── pdf_processor.py
├── utils/                       # Utilitaires
│   ├── __init__.py
│   ├── file_utils.py
│   └── image_utils.py
├── ui/                          # Interface utilisateur
│   ├── __init__.py
│   ├── main_window.py
│   └── components/
│       ├── __init__.py
│       ├── pdf_selection_panel.py
│       ├── processing_panel.py
│       ├── export_panel.py
│       └── success_dialog.py
└── controller/                  # Contrôleur principal
    ├── __init__.py
    └── app_controller.py
```

## Composants principaux

### 1. Models (`src/models/`)

- **PDFDocument**: Représente un document PDF avec ses propriétés
- **CombinedDocument**: Représente le résultat de la combinaison
- **ExportConfig**: Configuration pour l'export
- **Orientation**: Enum pour les orientations

### 2. Core (`src/core/`)

- **PDFProcessor**: Classe principale pour le traitement des PDF
  - Chargement des PDF et pages blanches
  - Traitement des orientations
  - Combinaison des images
  - Export des résultats

### 3. UI (`src/ui/`)

- **MainWindow**: Fenêtre principale de l'application
- **Components**: Composants UI modulaires
  - **PDFSelectionPanel**: Sélection et aperçu des PDF
  - **ProcessingPanel**: Traitement et aperçu des résultats
  - **ExportPanel**: Configuration et export
  - **SuccessDialog**: Dialogue de succès

### 4. Controller (`src/controller/`)

- **AppController**: Contrôleur principal orchestrant l'application
  - Gestion des événements UI
  - Coordination entre les modèles et les vues
  - Traitement en arrière-plan

### 5. Utils (`src/utils/`)

- **file_utils.py**: Utilitaires pour la gestion des fichiers
- **image_utils.py**: Utilitaires pour le traitement d'images

### 6. Configuration (`src/config.py`)

- Configuration centralisée de l'application
- Paramètres de l'UI, traitement d'images, export, etc.

### 7. Exceptions (`src/exceptions.py`)

- Exceptions personnalisées pour une meilleure gestion d'erreurs

## Avantages de cette architecture

### 1. Séparation des responsabilités

- **Modèles**: Gestion des données
- **Vues**: Interface utilisateur
- **Contrôleur**: Logique de coordination
- **Core**: Logique métier

### 2. Maintenabilité

- Code modulaire et organisé
- Faible couplage entre les composants
- Facile à tester et déboguer

### 3. Extensibilité

- Nouveaux formats d'export faciles à ajouter
- Nouveaux composants UI modulaires
- Nouvelles fonctionnalités isolées

### 4. Réutilisabilité

- Utilitaires réutilisables
- Composants UI indépendants
- Processeurs métier modulaires

### 5. Configuration centralisée

- Tous les paramètres dans un seul endroit
- Facile à modifier et maintenir

## Flux d'exécution

1. **Démarrage** (`main.py`)

   - Initialise le contrôleur principal
   - Lance l'application

2. **Initialisation** (`AppController`)

   - Crée le processeur PDF
   - Crée la fenêtre principale
   - Configure les callbacks

3. **Interaction utilisateur**

   - L'utilisateur interagit avec l'UI
   - Les événements sont capturés par les composants
   - Les callbacks sont envoyés au contrôleur

4. **Traitement**

   - Le contrôleur orchestre les opérations
   - Le processeur PDF effectue le traitement
   - L'UI est mise à jour en temps réel

5. **Export**
   - Configuration de l'export via l'UI
   - Traitement par le processeur
   - Affichage du résultat

## Gestion des erreurs

- Exceptions personnalisées pour chaque type d'erreur
- Gestion centralisée dans le contrôleur
- Messages d'erreur appropriés pour l'utilisateur
- Logging des erreurs pour le débogage

## Threading

- Traitement PDF en arrière-plan
- Interface utilisateur responsive
- Mise à jour de la progression en temps réel
- Gestion thread-safe des callbacks UI

## Points d'extension

1. **Nouveaux formats**: Ajouter dans `image_utils.py`
2. **Nouveaux composants UI**: Créer dans `ui/components/`
3. **Nouvelles fonctionnalités**: Étendre `PDFProcessor`
4. **Nouvelles configurations**: Ajouter dans `config.py`

Cette architecture permet une maintenance et une évolution faciles du code à long terme.
