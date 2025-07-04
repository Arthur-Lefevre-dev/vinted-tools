# Combinateur PDF - Moitiés

Application Python avec interface graphique pour combiner les moitiés de deux fichiers PDF A4 et les exporter en PNG.

## Fonctionnalités

- **Interface graphique intuitive** : Sélection facile des fichiers PDF
- **Aperçu en temps réel** : Visualisation des PDF sélectionnés
- **Combinaison automatique** :
  - Première image : Moitié haute du PDF 1 + Moitié basse du PDF 2
  - Seconde image : Moitié haute du PDF 2 + Moitié basse du PDF 1
- **Export PNG** : Sauvegarde en format PNG haute qualité

## Installation

### Prérequis

1. **Python 3.7+** installé sur votre système
2. **Poppler** (pour pdf2image) :
   - **Windows** : Téléchargez depuis [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/) et ajoutez le dossier `bin` à votre PATH
   - **macOS** : `brew install poppler`
   - **Linux** : `sudo apt-get install poppler-utils` (Ubuntu/Debian) ou `sudo yum install poppler-utils` (CentOS/RHEL)

### Installation des dépendances Python

```bash
pip install -r requirements.txt
```

## Utilisation

### Lancement de l'application

```bash
python pdf_combiner.py
```

### Étapes d'utilisation

1. **Sélectionner les PDF** : Cliquez sur "Parcourir" pour sélectionner vos deux fichiers PDF A4
2. **Aperçu** : Visualisez les PDF sélectionnés dans la zone d'aperçu
3. **Combiner** : Cliquez sur "Combiner et Exporter en PNG"
4. **Sauvegarder** : Choisissez le dossier de destination pour vos images PNG

### Résultats

L'application génère deux fichiers PNG :

- `PDF1_top_PDF2_bottom.png` : Moitié haute du premier PDF + Moitié basse du second PDF
- `PDF2_top_PDF1_bottom.png` : Moitié haute du second PDF + Moitié basse du premier PDF

## Exemple d'utilisation

Supposons que vous ayez deux fichiers :

- `document1.pdf` (contient du texte en haut et une image en bas)
- `document2.pdf` (contient une image en haut et du texte en bas)

L'application créera :

- `document1_top_document2_bottom.png` : Texte du document1 + Texte du document2
- `document2_top_document1_bottom.png` : Image du document2 + Image du document1

## Dépannage

### Erreur "pdf2image n'est pas installé"

Installez les dépendances avec : `pip install -r requirements.txt`

### Erreur "Unable to get page count"

Vérifiez que Poppler est correctement installé et accessible dans votre PATH.

### Problèmes de performance

Pour des PDF volumineux, l'application peut prendre quelques secondes. La barre de progression indique que le traitement est en cours.

## Fonctionnalités techniques

- **Redimensionnement intelligent** : Ajustement automatique de la largeur des images
- **Haute qualité** : Conversion PDF à 200 DPI pour une qualité optimale
- **Gestion d'erreurs** : Messages d'erreur clairs en cas de problème
- **Interface responsive** : Barre de progression et statut en temps réel

## Licence

Ce projet est libre d'utilisation pour un usage personnel et commercial.
