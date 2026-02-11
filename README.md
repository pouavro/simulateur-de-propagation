---
Auteur: Ilan Vast
title: Modèle de README pour les trophées NSI 
tags: trophées NSI, lycée
---

# 🚀 Simulateur de Propagation (Épidémie sur Grille)

## 📝 Description

Ce projet est un simulateur interactif développé en Python, modélisant la propagation d'une épidémie au sein d'une population sur une grille 2D. L'objectif est d'observer comment un virus se transmet entre l'environnement (les cases) et des individus mobiles (les personnages).

Le projet permet d'ajuster des probabilités de contamination et de visualiser en temps réel l'impact du contact social sur la vitesse d'infection. Il répond aux critères des Trophées NSI en combinant une interface graphique dynamique avec une gestion rigoureuse des structures de données.

## 👥 L'Équipe

- **Ilan Vast** (@pouavro) : 
- **Lucas** (à remplir) :

## 🛠️ Aspects Techniques (Spécificités NSI)

Cette section détaille les concepts du programme de NSI exploités dans ce projet :

- **Langages & Libs :** Python 3 et la bibliothèque **Tkinter** (interface graphique et gestion d'événements).
- **Structures de données :** - **Dictionnaires :** Utilisation de `cases = {}` associant des coordonnées `(lig, col)` à des identifiants d'objets Canvas pour un accès en temps constant $O(1)$.
  - **Listes de listes :** La population est gérée par une liste `liste_personnages = []` où chaque élément est une liste `[id_canvas, ligne, colonne, etat]`. Cette structure permet de modifier dynamiquement les attributs d'un individu.
  - **Sets (Ensembles) :** Utilisation de `set()` pour stocker les nouveaux infectés lors d'un tour, évitant ainsi les doublons et les redondances de calcul.
- **Concepts mobilisés :**
  - **Modélisation de voisinage :** Calcul de "hitbox" par vecteurs de déplacement `directions = [(0, 0), (-1, 0), ...]` pour simuler la zone de contact autour d'un personnage.
  - **Boucle événementielle :** Gestion de la simulation asynchrone via la méthode `.after()` de Tkinter.
  - **Traitement d'image :** Redimensionnement et intégration de ressources graphiques externes avec `PhotoImage`.



## 🚀 Installation et Utilisation

Expliquez comment tester votre projet :

1. **Prérequis :** Python 3.8+
2. **Installation :** Téléchargez le script et assurez-vous que l'image `perso 1.png` se trouve dans le même dossier.
3. **Lancement :** ```bash
   python main.py
