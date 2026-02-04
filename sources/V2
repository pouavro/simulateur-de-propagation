import tkinter as tk
import random 

# ────────────── CONFIGURATION GLOBALE ──────────────
# On fixe la taille du Canvas (zone de dessin) en pixels.
# Elle ne changera jamais, même si on change le nombre de cases.
CANVAS_SIZE = 700  

class SimulateurPro:
    def __init__(self, root):
        """
        Constructeur de l'application : initialise la fenêtre, 
        les variables et l'interface.
        """
        self.root = root
        self.root.title("Epidemic Simulator Pro - NSI Edition")
        
        # Définition d'une fenêtre large (16:9) pour un aspect "Dashboard"
        self.root.geometry("1400x820")
        self.root.configure(bg="#0f172a") # Couleur de fond bleu nuit (Slate 900)

        # --- VARIABLES DE CONTRÔLE DE LA SIMULATION ---
        # IntVar est une variable spéciale Tkinter liée au menu de sélection de taille
        self.nb_cases = tk.IntVar(value=20) 
        self.auto_running = False  # Booléen pour savoir si la simulation tourne en boucle
        self.confinement = False   # Booléen pour l'état du mode confinement
        
        # --- STRUCTURES DE DONNÉES ---
        # On utilise des dictionnaires pour lier les coordonnées (ligne, colonne) aux données
        self.etats = {}  # { (0,0): 'S', (0,1): 'I', ... } -> Stocke l'état de chaque case
        self.rects = {}  # { (0,0): id1, (0,1): id2, ... } -> Stocke l'identifiant graphique Tkinter

        # Code couleur hexadécimal pour chaque état
        self.colors = {
            'S': "#22c55e", # Sain (Vert)
            'I': "#ef4444", # Infecté (Rouge)
            'R': "#3b82f6", # Immunisé/Rétabli (Bleu)
            'V': "#475569"  # Vide ou Vacciné (Gris)
        }

        # Lancement de la construction de l'interface et de la grille initiale
        self.setup_layout()
        self.reset_grille()

    def setup_layout(self):
        """
        Crée l'organisation visuelle de la fenêtre (Panneau gauche vs Panneau droit)
        """
        # --- BLOC GAUCHE : LA GRILLE ---
        self.frame_left = tk.Frame(self.root, bg="#0f172a")
        self.frame_left.pack(side="left", expand=True, fill="both", padx=20, pady=20)

        # Création de la zone de dessin (Canvas)
        self.canvas = tk.Canvas(
            self.frame_left, 
            width=CANVAS_SIZE, height=CANVAS_SIZE, 
            bg="#1e293b", # Fond de la grille (Slate 800)
            highlightthickness=0
        )
        self.canvas.pack(expand=True)

        # --- BLOC DROIT : LE PANNEAU DE CONTRÔLE ---
        self.frame_right = tk.Frame(self.root, bg="#1e293b", width=380)
        self.frame_right.pack(side="right", fill="y")
        self.frame_right.pack_propagate(False) # Force la largeur à 380px

        # Titre du Dashboard
        tk.Label(self.frame_right, text="DASHBOARD", font=("Impact", 28), fg="#f8fafc", bg="#1e293b").pack(pady=20)

        # Conteneur interne pour les éléments du menu (avec marges)
        self.controls = tk.Frame(self.frame_right, bg="#1e293b", padx=30)
        self.controls.pack(fill="both")

        # --- SÉLECTEUR DE TAILLE ---
        tk.Label(self.controls, text="TAILLE DE LA MAP", fg="#94a3b8", bg="#1e293b", font=("Arial", 10, "bold")).pack(anchor="w")
        tailles_possibles = [10, 20, 50] 
        # OptionMenu permet de choisir la taille. Le changement appelle reset_grille()
        self.menu_taille = tk.OptionMenu(self.controls, self.nb_cases, *tailles_possibles, command=lambda _: self.reset_grille())
        self.menu_taille.config(bg="#334155", fg="white", relief="flat", highlightthickness=0)
        self.menu_taille.pack(fill="x", pady=(5, 20))

        # --- SLIDERS (PARAMÈTRES MATHÉMATIQUES) ---
        self.slider_immune = self.create_styled_slider("Immunité Pop. (%)", 0, 100, 15)
        self.slider_inf = self.create_styled_slider("Taux de contagion", 0, 1, 0.4, res=0.01)
        self.slider_guerison = self.create_styled_slider("Vitesse de guérison", 0, 1, 0.1, res=0.01)

        # --- BOUTONS D'ACTION ---
        self.btn_auto = self.create_btn("LANCER SIMULATION", "#22c55e", self.toggle_auto)
        self.create_btn("ÉTAPE SUIVANTE", "#3b82f6", self.propagation)
        self.btn_conf = self.create_btn("CONFINEMENT : OFF", "#f59e0b", self.toggle_confinement)
        self.create_btn("RÉGÉNÉRER MAP", "#ef4444", self.reset_grille)

        # --- ZONE DE STATISTIQUES (BAS DU PANNEAU) ---
        self.stats_label = tk.Label(self.frame_right, text="", font=("Consolas", 12), fg="#94a3b8", bg="#1e293b", justify="left")
        self.stats_label.pack(side="bottom", pady=30)

        # Événement : clic gauche sur le canvas = infection manuelle
        self.canvas.bind("<Button-1>", self.clic_gauche)

    def reset_grille(self):
        """
        Réinitialise totalement la grille : supprime les anciens carrés 
        et en crée de nouveaux selon la taille choisie.
        """
        self.auto_running = False # On stoppe l'auto-simulation
        self.btn_auto.config(text="LANCER SIMULATION", bg="#22c55e")
        
        self.canvas.delete("all") # On efface tout le dessin actuel
        self.etats.clear()        # On vide les dictionnaires de données
        self.rects.clear()
        
        n = self.nb_cases.get()       # Récupère 10, 20 ou 50
        self.taille_case = CANVAS_SIZE / n # Calcule la taille d'un carré en pixels
        seuil_immunite = self.slider_immune.get() / 100 # Probabilité d'être immunisé au départ
        
        # Double boucle pour générer la grille (lignes et colonnes)
        for i in range(n):
            for j in range(n):
                # Calcul des coordonnées de chaque coin du carré
                x1, y1 = j * self.taille_case, i * self.taille_case
                x2, y2 = x1 + self.taille_case, y1 + self.taille_case
                
                # Détermination aléatoire de l'état initial (Sain ou déjà Immunisé)
                etat_init = 'R' if random.random() < seuil_immunite else 'S'
                
                # Création de l'objet graphique sur le Canvas
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill=self.colors[etat_init], 
                    outline="#0f172a" # Bordure très fine
                )
                
                # Enregistrement dans les dictionnaires
                self.etats[(i, j)] = etat_init
                self.rects[(i, j)] = rect_id
        
        self.maj_stats() # Mise à jour de l'affichage des compteurs

    def propagation(self):
        """
        LOGIQUE ALGORITHMIQUE : Calcule le passage à l'étape suivante.
        Applique les règles de contagion et de guérison.
        """
        # On réduit la contagion si le confinement est actif
        p_inf = self.slider_inf.get() / (3 if self.confinement else 1)
        p_rec = self.slider_guerison.get()
        
        # Dictionnaire temporaire pour stocker les futurs changements
        # (Indispensable pour ne pas modifier la grille pendant qu'on la parcourt)
        changements = {}

        # On récupère uniquement les coordonnées des personnes actuellement malades ('I')
        infectes = [coord for coord, etat in self.etats.items() if etat == 'I']
        
        # Sécurité : Si plus de malades, on arrête la simulation automatique
        if not infectes and self.auto_running:
            self.toggle_auto()
            return

        # Pour chaque malade, on tente d'infecter ses voisins
        for (l, c) in infectes:
            # Liste des 8 voisins (Voisinage de Moore : haut, bas, gauche, droite + diagonales)
            directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            for dl, dc in directions:
                voisin = (l + dl, c + dc)
                
                # Si le voisin existe et qu'il est Sain ('S')
                if voisin in self.etats and self.etats[voisin] == 'S':
                    # On tire un nombre aléatoire entre 0 et 1
                    if random.random() < p_inf:
                        changements[voisin] = 'I' # Il devient infecté
            
            # Tentative de guérison du malade actuel
            if random.random() < p_rec:
                changements[(l, c)] = 'R' # Il devient rétabli/immunisé

        # Application des changements stockés
        for coord, nouvel_etat in changements.items():
            self.etats[coord] = nouvel_etat
            # On met à jour la couleur du carré correspondant sur le Canvas
            self.canvas.itemconfig(self.rects[coord], fill=self.colors[nouvel_etat])
        
        self.maj_stats()

    def clic_gauche(self, event):
        """
        Permet d'infecter manuellement une case au clic de la souris.
        """
        # On convertit les pixels du clic en coordonnées (ligne, colonne)
        l = int(event.y // self.taille_case)
        c = int(event.x // self.taille_case)
        
        if (l, c) in self.etats:
            self.etats[(l, c)] = 'I'
            self.canvas.itemconfig(self.rects[(l, c)], fill=self.colors['I'])
            self.maj_stats()

    def create_styled_slider(self, txt, mini, maxi, dft, res=1):
        """
        Aide visuelle : Crée un label + un curseur (Scale) stylisé.
        """
        tk.Label(self.controls, text=txt, fg="#94a3b8", bg="#1e293b", font=("Arial", 10, "bold")).pack(anchor="w")
        s = tk.Scale(self.controls, from_=mini, to=maxi, resolution=res, orient="horizontal", 
                     bg="#1e293b", fg="white", highlightthickness=0, troughcolor="#334155",
                     activebackground="#3b82f6")
        s.set(dft)
        s.pack(fill="x", pady=(0, 15))
        return s

    def create_btn(self, txt, color, cmd):
        """
        Aide visuelle : Crée un bouton avec un style moderne.
        """
        btn = tk.Button(self.controls, text=txt, command=cmd, bg=color, fg="white",
                        font=("Arial", 10, "bold"), relief="flat", pady=8, cursor="hand2")
        btn.pack(fill="x", pady=5)
        return btn

    def toggle_auto(self):
        """
        Active ou désactive le mode automatique.
        """
        self.auto_running = not self.auto_running
        if self.auto_running:
            self.btn_auto.config(text="STOPPER LA SIMU", bg="#ef4444")
            self.run_loop() # Lance la boucle
        else:
            self.btn_auto.config(text="LANCER SIMULATION", bg="#22c55e")

    def run_loop(self):
        """
        La boucle temporelle : s'appelle elle-même toutes les 50 millisecondes.
        """
        if self.auto_running:
            self.propagation() # Fait une étape
            # .after(temps, fonction) est la méthode Tkinter pour créer une boucle
            self.root.after(50, self.run_loop) 

    def toggle_confinement(self):
        """
        Active ou désactive le confinement pour modifier les calculs de propagation.
        """
        self.confinement = not self.confinement
        if self.confinement:
            self.btn_conf.config(text="CONFINEMENT : ON", bg="#ef4444")
        else:
            self.btn_conf.config(text="CONFINEMENT : OFF", bg="#f59e0b")

    def maj_stats(self):
        """
        Calcule le nombre de cases dans chaque état et met à jour l'étiquette texte.
        """
        # On récupère toutes les valeurs du dictionnaire etats
        valeurs = list(self.etats.values())
        sains = valeurs.count('S')
        infectes = valeurs.count('I')
        gueris = valeurs.count('R')
        
        # Mise à jour du texte avec une police à espacement fixe (Consolas)
        self.stats_label.config(text=f"SAINS: {sains}\nINFECTÉS: {infectes}\nGUÉRIS: {gueris}")

# --- LANCEMENT DU PROGRAMME ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SimulateurPro(root)
    root.mainloop() # Lance la gestion des événements Tkinter




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
