import tkinter as tk
import random

# ────────────── Configuration Grand Écran ──────────────
NB_CASES_COTE = 45   # Plus de cases pour remplir l'écran
DENSITE_GRILLE = 0.85 # Pourcentage de l'écran occupé par la grille

class SimulateurPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Epidemic Simulator Pro - NSI Edition")
        
        # Force le mode plein écran ou une grande fenêtre 16:9
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # On définit une taille large par défaut (ex: 1400x800)
        win_w, win_h = 1400, 800
        self.root.geometry(f"{win_w}x{win_h}")
        self.root.configure(bg="#0f172a") # Bleu nuit très sombre

        # Calcul dynamique de la taille des cases
        self.taille_case = (win_h * DENSITE_GRILLE) // NB_CASES_COTE
        
        self.auto_running = False
        self.confinement = False
        self.etats = {}
        self.rects = {}

        self.colors = {
            'S': "#22c55e", # Vert flashy
            'I': "#ef4444", # Rouge vif
            'R': "#3b82f6", # Bleu néon
            'V': "#475569"  # Ardoise (vide/vacciné)
        }

        self.setup_layout()
        self.reset_grille()

    def setup_layout(self):
        # --- PANNEAU GAUCHE (LA GRILLE) ---
        self.frame_left = tk.Frame(self.root, bg="#0f172a")
        self.frame_left.pack(side="left", expand=True, fill="both", padx=20, pady=20)

        canvas_size = NB_CASES_COTE * self.taille_case
        self.canvas = tk.Canvas(
            self.frame_left, 
            width=canvas_size, 
            height=canvas_size, 
            bg="#1e293b", 
            highlightthickness=0
        )
        self.canvas.pack(expand=True)

        # --- PANNEAU DROIT (PARAMÈTRES) ---
        self.frame_right = tk.Frame(self.root, bg="#1e293b", width=350)
        self.frame_right.pack(side="right", fill="y", padx=0, pady=0)
        self.frame_right.pack_propagate(False) # Garde sa largeur de 350px

        # Titre stylé
        tk.Label(
            self.frame_right, text="DASHBOARD", 
            font=("Impact", 28), fg="#f8fafc", bg="#1e293b"
        ).pack(pady=30)

        # Conteneur pour les réglages (Padding interne)
        self.controls = tk.Frame(self.frame_right, bg="#1e293b", padx=30)
        self.controls.pack(fill="both")

        # Sliders avec style
        self.slider_immune = self.create_styled_slider("Immunité Pop. (%)", 0, 100, 15)
        self.slider_inf = self.create_styled_slider("Taux de contagion", 0, 1, 0.4, res=0.01)
        self.slider_guerison = self.create_styled_slider("Vitesse de guérison", 0, 1, 0.1, res=0.01)

        # Espace
        tk.Frame(self.controls, height=20, bg="#1e293b").pack()

        # Boutons larges
        self.btn_auto = self.create_btn("LANCER SIMULATION", "#22c55e", self.toggle_auto)
        self.btn_step = self.create_btn("ÉTAPE SUIVANTE", "#3b82f6", self.propagation)
        self.btn_conf = self.create_btn("CONFINEMENT : OFF", "#f59e0b", self.toggle_confinement)
        self.create_btn("RESET", "#ef4444", self.reset_grille)

        # Stats en bas
        self.stats_label = tk.Label(
            self.frame_right, text="", font=("Consolas", 12), 
            fg="#94a3b8", bg="#1e293b", justify="left"
        )
        self.stats_label.pack(side="bottom", pady=40)

    def create_styled_slider(self, txt, mini, maxi, dft, res=1):
        tk.Label(self.controls, text=txt, fg="#94a3b8", bg="#1e293b", font=("Arial", 10, "bold")).pack(anchor="w")
        s = tk.Scale(
            self.controls, from_=mini, to=maxi, resolution=res, 
            orient="horizontal", bg="#1e293b", fg="white", 
            highlightthickness=0, troughcolor="#334155", activebackground="#3b82f6"
        )
        s.set(dft)
        s.pack(fill="x", pady=(0, 15))
        return s

    def create_btn(self, txt, color, cmd):
        btn = tk.Button(
            self.controls, text=txt, command=cmd, bg=color, fg="white",
            font=("Arial", 11, "bold"), relief="flat", pady=10, cursor="hand2"
        )
        btn.pack(fill="x", pady=5)
        return btn

    def reset_grille(self):
        self.canvas.delete("all")
        self.etats.clear()
        self.rects.clear()
        
        seuil = self.slider_immune.get() / 100
        for i in range(NB_CASES_COTE):
            for j in range(NB_CASES_COTE):
                x1, y1 = j * self.taille_case, i * self.taille_case
                etat = 'R' if random.random() < seuil else 'S'
                
                r = self.canvas.create_rectangle(
                    x1, y1, x1+self.taille_case-1, y1+self.taille_case-1, 
                    fill=self.colors[etat], outline="#0f172a"
                )
                self.etats[(i, j)] = etat
                self.rects[(i, j)] = r
        self.maj_stats()

    def propagation(self):
        p_inf = self.slider_inf.get() / (3 if self.confinement else 1)
        p_rec = self.slider_guerison.get()
        
        nouveaux = self.etats.copy()
        # Voisinage de Moore
        v_coords = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        for (l, c), etat in self.etats.items():
            if etat == 'I':
                for dl, dc in v_coords:
                    nc = (l+dl, c+dc)
                    if nc in self.etats and self.etats[nc] == 'S':
                        if random.random() < p_inf: nouveaux[nc] = 'I'
                if random.random() < p_rec: nouveaux[(l, c)] = 'R'

        for coord, etat in nouveaux.items():
            if etat != self.etats[coord]:
                self.canvas.itemconfig(self.rects[coord], fill=self.colors[etat])
                self.etats[coord] = etat
        self.maj_stats()

    def toggle_auto(self):
        self.auto_running = not self.auto_running
        self.btn_auto.config(text="STOPPER" if self.auto_running else "LANCER SIMULATION",
                             bg="#ef4444" if self.auto_running else "#22c55e")
        if self.auto_running: self.run_loop()

    def run_loop(self):
        if self.auto_running:
            self.propagation()
            self.root.after(100, self.run_loop)

    def toggle_confinement(self):
        self.confinement = not self.confinement
        self.btn_conf.config(text="CONFINEMENT : ON" if self.confinement else "CONFINEMENT : OFF",
                             bg="#ef4444" if self.confinement else "#f59e0b")

    def maj_stats(self):
        val = list(self.etats.values())
        txt = f"Sains     : {val.count('S')}\n"
        txt += f"Infectés  : {val.count('I')}\n"
        txt += f"Immunisés : {val.count('R')}"
        self.stats_label.config(text=txt)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulateurPro(root)
    root.mainloop()




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
