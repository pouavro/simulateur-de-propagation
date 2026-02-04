import tkinter as tk  # Bibliothèque pour créer l'interface graphique
import random         # Bibliothèque pour générer des nombres aléatoires

# ────────────── Paramètres ──────────────
prob = 0.65   # Probabilité qu'une case soit "saine" au départ
prob1 = 0.33  # Probabilité qu'une case saine devienne infectée
TAILLE_GRILLE = 10  # Nombre de cases par côté de la grille
TAILLE_CASE = 60    # Taille d'une case en pixels

nombre_de_simulations = 0  # Compteur de tours de simulation
auto_running = False       # Indique si la simulation automatique est activée

# Liste des directions pour propager l'infection (droite, gauche, haut, bas, et soi-même)
directions = [
    (0, 0),   # La case elle-même
    (-1, 0),  # Haut
    (1, 0),   # Bas
    (0, -1),  # Gauche
    (0, 1)    # Droite
]

# ────────────── Fenêtre ──────────────
fenetre = tk.Tk()  # Création de la fenêtre principale
fenetre.title("Simulation de propagation")
fenetre.geometry(f"{TAILLE_GRILLE * TAILLE_CASE + 400}x{TAILLE_GRILLE * TAILLE_CASE}")
fenetre.configure(bg="#2c4260")  # Couleur de fond de la fenêtre

# ────────────── Panneau droite (paramètres) ──────────────
frame_param = tk.Frame(fenetre, bg="#1d2b3e")  # Panneau pour les boutons et stats
frame_param.pack(side="right", fill="both", expand=True)

frame_boutons = tk.Frame(frame_param, bg="#1d2b3e")  # Panneau pour les boutons
frame_boutons.pack(pady=20)

# Titre "Paramètres"
titre_param = tk.Label(
    frame_param,
    text="Paramètres",
    font=("Impact", 24),
    bg="#1d2b3e",
    fg="#ffffff"
)
titre_param.pack()

# Label pour afficher les statistiques (nombre de cases saines, infectées, immunisées)
label_stats = tk.Label(
    frame_param,
    text="Sains : 0\nInfectés : 0\nImmunisés : 0",
    font=("Arial", 14),
    bg="#1d2b3e",
    fg="#ffffff",
    justify="left"
)
label_stats.pack(pady=20)

# Bouton "Reset" pour réinitialiser la grille
bouton_test = tk.Button(
    frame_boutons, text="Reset", font=("Arial", 16),
    bg="#394867", fg="#ffffff"
)
bouton_test.pack(side="left", padx=20)

# Bouton "Simuler" pour faire une étape de propagation
bouton_propagation = tk.Button(
    frame_boutons, text="Simuler", font=("Arial", 15),
    bg="#394867", fg="#ffffff"
)
bouton_propagation.pack(side="left", padx=20)

# Bouton "Auto OFF" pour lancer ou arrêter la simulation automatique
bouton_auto = tk.Button(
    frame_boutons, text="Auto OFF", font=("Arial", 16),
    bg="#394867", fg="#ffffff"
)
bouton_auto.pack(side="left", padx=20)

# ────────────── Panneau gauche (grille) ──────────────
canvas = tk.Canvas(
    fenetre,
    width=TAILLE_GRILLE * TAILLE_CASE,
    height=TAILLE_GRILLE * TAILLE_CASE,
    bg="#778DA9"
)
canvas.pack(side="left")

# ────────────── Données ──────────────
cases = {}          # Toutes les cases de la grille
cases_soignees = {}  # Cases saines (vertes)
cases_infectees = {} # Cases infectées (rouges)

# ────────────── Fonctions ──────────────

# Met à jour les statistiques affichées
def maj_stats():
    # Immunisées = cases blanches (ni saines ni infectées)
    immunises = len(cases) - len(cases_soignees) - len(cases_infectees)
    label_stats.config(
        text=f"Sains : {len(cases_soignees)}\n"
             f"Infectés : {len(cases_infectees)}\n"
             f"Immunisés : {immunises}"
    )

# Initialise la grille avec des cases saines et des cases immunisées
def starting_grid():
    global nombre_de_simulations
    nombre_de_simulations = 0  # Remise à zéro du compteur

    cases.clear()
    cases_soignees.clear()
    cases_infectees.clear()
    canvas.delete("all")  # Efface le canvas pour repartir à zéro

    for i in range(TAILLE_GRILLE):
        for j in range(TAILLE_GRILLE):
            x1 = j * TAILLE_CASE
            y1 = i * TAILLE_CASE
            x2 = x1 + TAILLE_CASE
            y2 = y1 + TAILLE_CASE

            # On crée chaque case en blanc par défaut (immunisée)
            rect = canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="#f4f1de",  # Blanc = immunisée
                outline="#394867"
            )
            cases[(i, j)] = rect

            # On colore certaines cases en vert (saines) selon la probabilité 'prob'
            if random.random() < prob:
                canvas.itemconfig(rect, fill="#a7c957")
                cases_soignees[(i, j)] = rect

    maj_stats()  # Mise à jour des stats après initialisation

# Vérifie si la propagation est possible (s'il y a des cases saines autour des infectées)
def propagation_possible():
    for lig, col in cases_infectees:
        for dx, dy in directions:
            nl, nc = lig + dx, col + dy
            if (nl, nc) in cases_soignees:
                return True
    return False

# Fait une étape de propagation : les cases saines autour des infectées peuvent devenir infectées
def propagation():
    global nombre_de_simulations
    nombre_de_simulations += 1

    nouveaux_infectes = set()

    for lig, col in list(cases_infectees.keys()):
        for dx, dy in directions:
            nl, nc = lig + dx, col + dy
            if (nl, nc) in cases_soignees:
                if random.random() < prob1:  # Probabilité qu'une case saine devienne infectée
                    nouveaux_infectes.add((nl, nc))

    # On applique l'infection sur les nouvelles cases
    for coord in nouveaux_infectes:
        canvas.itemconfig(cases[coord], fill="#bc4749")  # Rouge = infecté
        cases_infectees[coord] = cases[coord]
        del cases_soignees[coord]

    maj_stats()

# Fonction pour faire tourner la simulation automatiquement
def propagation_auto():
    if not auto_running:
        return

    if propagation_possible():
        propagation()
        bouton_auto.config(text="Auto (propagation)", bg="#39673C")
    else:
        bouton_auto.config(text="Auto (en attente)", bg="#6c757d")

    fenetre.after(300, propagation_auto)  # Appelle cette fonction toutes les 0.3 secondes

# Active ou désactive la simulation automatique
def toggle_auto():
    global auto_running
    auto_running = not auto_running

    if auto_running:
        propagation_auto()
    else:
        bouton_auto.config(text="Auto OFF", bg="#394867")

# Fonction appelée au clic sur une case : infecte la case cliquée si elle est saine
def clic(event):
    lig = event.y // TAILLE_CASE
    col = event.x // TAILLE_CASE

    if (lig, col) in cases_soignees:
        canvas.itemconfig(cases[(lig, col)], fill="#bc4749")  # Rouge = infecté
        cases_infectees[(lig, col)] = cases[(lig, col)]
        del cases_soignees[(lig, col)]
        maj_stats()

# ────────────── Bindings ──────────────
bouton_test.config(command=starting_grid)        # Clique sur Reset
bouton_propagation.config(command=propagation)   # Clique sur Simuler
bouton_auto.config(command=toggle_auto)          # Clique sur Auto
canvas.bind("<Button-1>", clic)                  # Clique sur la grille

# ────────────── Lancement ──────────────
starting_grid()  # Initialisation de la grille au démarrage
fenetre.mainloop()  # Boucle principale Tkinter




# def propagation():
#     global nombre_de_simulations
#     nombre_de_simulations += 1
#     print(f"--- Simulation n°{nombre_de_simulations} ---")
#     if auto_running == False:
#         for infecte in list(cases_infectees.keys()):
#             lig, col = infecte
#             for dx, dy in directions:
#                 nl = lig + dx
#                 nc = col + dy
#                 if (nl, nc) in cases:
#                     if random.random() < prob1 and (nl, nc) in cases_soignees:
#                         canvas.itemconfig(cases[(nl, nc)], fill="#bc4749")
#                         cases_infectees[(nl, nc)] = cases[(nl, nc)]
#                         del cases_soignees[(nl, nc)]
#     else:
#          for infecte in list(cases_infectees.keys()):
#             lig, col = infecte
#             for dx, dy in directions:
#                 nl = lig + dx
#                 nc = col + dy
#                 if (nl, nc) in cases:
#                     ...
#                     if random.random() < prob1:
#                         canvas.itemconfig(cases[(nl, nc)], fill="#bc4749")
#                         cases_infectees[(nl, nc)] = cases[(nl, nc)]
#                         del cases_soignees[(nl, nc)]


### propgation aux alentour des case rouge

# fonction appelée au clic
# def clic(event):
#     col = event.x // TAILLE_CASE
#     lig = event.y // TAILLE_CASE
#     propagation()

#     for dx, dy in directions:
#         nl = lig + dx
#         nc = col + dy

#         if (nl, nc) in cases:
                
#             if random.random() < prob1 and (nl, nc) in cases_soignees:
#                 canvas.itemconfig(cases[(nl, nc)], fill="#bc4749")
#                 cases_infectees[(nl, nc)] = cases[(nl, nc)]
#                 del cases_soignees[(nl, nc)]
