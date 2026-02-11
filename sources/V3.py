import tkinter as tk
import random

# ────────────── CONFIGURATION GLOBALE ──────────────
CANVAS_SIZE = 700  # Taille de la fenêtre de dessin
nb_cases = 20      # Taille par défaut (20x20)
taille_case = CANVAS_SIZE / nb_cases

# Dictionnaires globaux pour stocker les données
etats = {}  # Stocke l'état : (ligne, col) -> "S", "I" ou "R"
rects = {}  # Stocke l'objet graphique : (ligne, col) -> ID du carré
auto_running = False
confinement = False

# Couleurs
COLORS = {'S': "#22c55e", 'I': "#ef4444", 'R': "#3b82f6"}

# ────────────── FONCTIONS DE LOGIQUE ──────────────

def initialiser_grille():
    """ Crée les carrés et remplit les dictionnaires """
    global taille_case, auto_running
    auto_running = False
    btn_auto.config(text="LANCER SIMULATION", bg="#22c55e")
    
    canvas.delete("all")
    etats.clear()
    rects.clear()
    
    n = int(liste_taille.get()) # On récupère la taille choisie dans le menu
    taille_case = CANVAS_SIZE / n
    seuil_immune = slider_immune.get() / 100
    
    for l in range(n):
        for c in range(n):
            x1, y1 = c * taille_case, l * taille_case
            x2, y2 = x1 + taille_case, y1 + taille_case
            
            # Tirage au sort de l'état initial
            etat = 'R' if random.random() < seuil_immune else 'S'
            
            # Dessin
            rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill=COLORS[etat], outline="#0f172a")
            
            # Enregistrement
            etats[(l, c)] = etat
            rects[(l, c)] = rect_id
    maj_stats()

def propagation():
    """ Calcule une étape de l'épidémie """
    # Probabilité réduite si confinement actif
    p_inf = slider_inf.get() / (3 if confinement else 1)
    p_rec = slider_guerison.get()
    
    changements = {}
    
    # On cherche les malades
    for coord, etat in etats.items():
        if etat == 'I':
            l, c = coord
            # Voisinage de Moore (8 directions)
            for dl, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                v = (l + dl, c + dc)
                if v in etats and etats[v] == 'S':
                    if random.random() < p_inf:
                        changements[v] = 'I'
            
            # Guérison
            if random.random() < p_rec:
                changements[coord] = 'R'
    
    # Appliquer les changements
    for coord, nouvel_etat in changements.items():
        etats[coord] = nouvel_etat
        canvas.itemconfig(rects[coord], fill=COLORS[nouvel_etat])
    
    maj_stats()

def maj_stats():
    """ Met à jour le texte des scores """
    liste_etats = list(etats.values())
    s = liste_etats.count('S')
    i = liste_etats.count('I')
    r = liste_etats.count('R')
    label_stats.config(text=f"SAINS: {s} | INFECTÉS: {i} | GUÉRIS: {r}")

# ────────────── GESTION DES ÉVÉNEMENTS ──────────────

def clic_canvas(event):
    """ Infecte une case au clic """
    l = int(event.y // taille_case)
    c = int(event.x // taille_case)
    if (l, c) in etats:
        etats[(l, c)] = 'I'
        canvas.itemconfig(rects[(l, c)], fill=COLORS['I'])
        maj_stats()

def toggle_auto():
    global auto_running
    auto_running = not auto_running
    if auto_running:
        btn_auto.config(text="STOPPER", bg="#ef4444")
        boucle_simu()
    else:
        btn_auto.config(text="LANCER SIMULATION", bg="#22c55e")

def boucle_simu():
    if auto_running:
        propagation()
        fenetre.after(50, boucle_simu)

def toggle_confinement():
    global confinement
    confinement = not confinement
    btn_conf.config(text="CONFINEMENT: ON" if confinement else "CONFINEMENT: OFF", 
                    bg="#ef4444" if confinement else "#f59e0b")

# ────────────── INTERFACE GRAPHIQUE ──────────────

fenetre = tk.Tk()
fenetre.title("Simulateur Épidémie - NSI")
fenetre.geometry("1100x750")
fenetre.configure(bg="#0f172a")

# Canvas à gauche
canvas = tk.Canvas(fenetre, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="#1e293b", highlightthickness=0)
canvas.pack(side="left", padx=10, pady=10)
canvas.bind("<Button-1>", clic_canvas)

# Menu à droite
menu = tk.Frame(fenetre, bg="#1e293b", padx=20)
menu.pack(side="right", fill="both", expand=True)

# Sélecteur de taille
tk.Label(menu, text="TAILLE DE LA GRILLE", fg="white", bg="#1e293b").pack(pady=5)
liste_taille = tk.StringVar(value="20")
selecteur = tk.OptionMenu(menu, liste_taille, "10", "20", "50", command=lambda _: initialiser_grille())
selecteur.pack(fill="x", pady=5)

# Sliders
slider_immune = tk.Scale(menu, from_=0, to=100, label="Immunité initiale %", orient="horizontal", bg="#1e293b", fg="white")
slider_immune.set(15)
slider_immune.pack(fill="x")

slider_inf = tk.Scale(menu, from_=0, to=1, resolution=0.01, label="Taux d'infection", orient="horizontal", bg="#1e293b", fg="white")
slider_inf.set(0.4)
slider_inf.pack(fill="x")

slider_guerison = tk.Scale(menu, from_=0, to=1, resolution=0.01, label="Taux de guérison", orient="horizontal", bg="#1e293b", fg="white")
slider_guerison.set(0.1)
slider_guerison.pack(fill="x")

# Boutons
btn_auto = tk.Button(menu, text="LANCER SIMULATION", bg="#22c55e", fg="white", command=toggle_auto)
btn_auto.pack(fill="x", pady=5)

tk.Button(menu, text="ÉTAPE PAR ÉTAPE", command=propagation).pack(fill="x", pady=5)

btn_conf = tk.Button(menu, text="CONFINEMENT: OFF", bg="#f59e0b", fg="white", command=toggle_confinement)
btn_conf.pack(fill="x", pady=5)

tk.Button(menu, text="RELIRE / RESET", bg="#ef4444", fg="white", command=initialiser_grille).pack(fill="x", pady=5)

label_stats = tk.Label(menu, text="", fg="white", bg="#1e293b", font=("Arial", 12))
label_stats.pack(side="bottom", pady=20)

initialiser_grille()
fenetre.mainloop()
