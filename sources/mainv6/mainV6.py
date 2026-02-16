import tkinter as tk
import random

# ────────────── PARAMÈTRES INITIAUX ──────────────
TAILLE_GRILLE = 15   
TAILLE_CASE = 50   
NB_PERSONNAGES = 10 # Augmenté un peu pour voir l'effet
NB_INFECTES_DEPART = 3 
PROB_SAIN_DEPART = 0.8

auto_running = False

COLORS = {
    'S': "#a7c957", 
    'F': "#f4f1de", 
    'H_SAIN': "#90e0ef", 
    'H_INFECTE': "#ffb3c1" 
}

directions = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

# ────────────── FENÊTRE ──────────────
fenetre = tk.Tk()
fenetre.title("Simulation Épidémique : Mortalité")
largeur_canvas = TAILLE_GRILLE * TAILLE_CASE
fenetre.geometry(f"{largeur_canvas + 400}x{largeur_canvas + 100}")
fenetre.configure(bg="#2c4260")

# ────────────── PANNEAU DROITE ──────────────
frame_param = tk.Frame(fenetre, bg="#1d2b3e")
frame_param.pack(side="right", fill="both", expand=True)

tk.Label(frame_param, text="LABORATOIRE NSI", font=("Impact", 24), bg="#1d2b3e", fg="#ffffff").pack(pady=10)

# --- Curseurs ---
tk.Label(frame_param, text="Vitesse Déplacement %", font=("Arial", 10, "bold"), bg="#1d2b3e", fg="#ffffff").pack()
curseur_vitesse = tk.Scale(frame_param, from_=0, to=100, orient="horizontal", bg="#1d2b3e", fg="#ffffff", highlightthickness=0, length=250)
curseur_vitesse.set(50)
curseur_vitesse.pack(pady=5)

# NOUVEAU : Curseur pour la probabilité de mourir
tk.Label(frame_param, text="Probabilité de Mourir %", font=("Arial", 10, "bold"), bg="#1d2b3e", fg="#ffffff").pack()
curseur_mort = tk.Scale(frame_param, from_=0, to=20, orient="horizontal", bg="#1d2b3e", fg="#ffffff", highlightthickness=0, length=250)
curseur_mort.set(5) # 5% par tour par défaut
curseur_mort.pack(pady=5)

label_stats = tk.Label(frame_param, text="", font=("Arial", 12), bg="#1d2b3e", fg="#ffffff", justify="left")
label_stats.pack(pady=20)

# ────────────── CANVAS ──────────────
canvas = tk.Canvas(fenetre, width=largeur_canvas, height=largeur_canvas, bg="#778DA9", highlightthickness=0)
canvas.pack(side="left", padx=10, pady=10)

try:
    img_bonhomme = tk.PhotoImage(file="perso 1.png")
    img_bonhomme = img_bonhomme.subsample(max(1, img_bonhomme.width() // 40)) 
except: img_bonhomme = None

# ────────────── DONNÉES ──────────────
etats_sol = {}; rects = {}; persos = {}

# ────────────── FONCTIONS OUTILS ──────────────

def infecter_personnage(pid):
    if pid in persos: persos[pid]['etat'] = "infecte"

def tuer_personnage(pid):
    if pid in persos:
        canvas.delete(pid)
        del persos[pid]

def obtenir_hitbox(pid):
    p = persos[pid]
    return [(p['lig']+dl, p['col']+dc) for dl, dc in directions if 0 <= p['lig']+dl < TAILLE_GRILLE and 0 <= p['col']+dc < TAILLE_GRILLE]

def verifier_collision(id1, id2):
    return not set(obtenir_hitbox(id1)).isdisjoint(set(obtenir_hitbox(id2)))

# ────────────── LOGIQUE DE SIMULATION ──────────────

def gerer_mortalite():
    """Chaque infecté a une chance de mourir à ce tour."""
    prob_actuelle = curseur_mort.get() / 100
    # On fait une copie de la liste des IDs pour éviter les erreurs pendant la suppression
    tous_les_pids = list(persos.keys())
    
    for pid in tous_les_pids:
        if pid in persos and persos[pid]['etat'] == "infecte":
            if random.random() < prob_actuelle:
                tuer_personnage(pid)

def gerer_collisions():
    pids = list(persos.keys())
    for i in range(len(pids)):
        for j in range(i + 1, len(pids)):
            id1, id2 = pids[i], pids[j]
            if id1 in persos and id2 in persos:
                if (persos[id1]['etat'] == "infecte") != (persos[id2]['etat'] == "infecte"):
                    if verifier_collision(id1, id2):
                        infecter_personnage(id1)
                        infecter_personnage(id2)

def deplacer_tous():
    v_prob = curseur_vitesse.get() / 100
    for pid, data in persos.items():
        if random.random() < v_prob:
            dl, dc = random.choice([(-1,0), (1,0), (0,-1), (0,1)])
            nl, nc = data['lig'] + dl, data['col'] + dc
            if 0 <= nl < TAILLE_GRILLE and 0 <= nc < TAILLE_GRILLE:
                data['lig'], data['col'] = nl, nc
                canvas.coords(pid, nc*TAILLE_CASE + TAILLE_CASE//2, nl*TAILLE_CASE + TAILLE_CASE//2)

def rafraichir_visuel():
    for coord, etat in etats_sol.items():
        canvas.itemconfig(rects[coord], fill=COLORS[etat])
    for pid, data in persos.items():
        couleur = COLORS['H_INFECTE'] if data['etat'] == "infecte" else COLORS['H_SAIN']
        for coord in obtenir_hitbox(pid):
            canvas.itemconfig(rects[coord], fill=couleur)

def maj_stats():
    s = sum(1 for p in persos.values() if p['etat'] == "sain")
    i = sum(1 for p in persos.values() if p['etat'] == "infecte")
    label_stats.config(text=f"SAINS : {s}\nINFECTÉS : {i}\nTOTAL VIVANTS : {len(persos)}")

def propagation():
    if not persos: return # Plus personne en vie
    deplacer_tous()
    gerer_collisions()
    gerer_mortalite() # <--- Appel de la nouvelle fonction
    rafraichir_visuel()
    maj_stats()

# ────────────── BOUCLE ET BOUTONS ──────────────

def boucle_auto():
    if auto_running:
        propagation()
        fenetre.after(100, boucle_auto)

def toggle_auto():
    global auto_running
    auto_running = not auto_running
    btn_auto.config(text="STOP" if auto_running else "AUTO", bg="#ef4444" if auto_running else "#394867")
    if auto_running: boucle_auto()

def starting_grid():
    global auto_running
    auto_running = False
    canvas.delete("all")
    etats_sol.clear(); rects.clear(); persos.clear()
    
    for l in range(TAILLE_GRILLE):
        for c in range(TAILLE_GRILLE):
            etat = 'S' if random.random() < PROB_SAIN_DEPART else 'F'
            rects[(l, c)] = canvas.create_rectangle(c*TAILLE_CASE, l*TAILLE_CASE, (c+1)*TAILLE_CASE, (l+1)*TAILLE_CASE, fill=COLORS[etat], outline="#394867")
            etats_sol[(l, c)] = etat

    all_pids = []
    for _ in range(NB_PERSONNAGES):
        l, c = random.randint(0, TAILLE_GRILLE-1), random.randint(0, TAILLE_GRILLE-1)
        pid = canvas.create_image(c*TAILLE_CASE + TAILLE_CASE//2, l*TAILLE_CASE + TAILLE_CASE//2, image=img_bonhomme)
        persos[pid] = {'lig': l, 'col': c, 'etat': "sain"}
        all_pids.append(pid)

    for i in range(min(NB_INFECTES_DEPART, len(all_pids))):
        infecter_personnage(all_pids[i])

    rafraichir_visuel()
    maj_stats()

# ────────────── INTERFACE ──────────────
frame_btns = tk.Frame(frame_param, bg="#1d2b3e")
frame_btns.pack(pady=10)
tk.Button(frame_btns, text="Reset", command=starting_grid).pack(side="left", padx=5)
tk.Button(frame_btns, text="Tour suivant", command=propagation).pack(side="left", padx=5)
btn_auto = tk.Button(frame_btns, text="AUTO", command=toggle_auto)
btn_auto.pack(side="left", padx=5)

starting_grid()
fenetre.mainloop()
