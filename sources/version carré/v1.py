import sys
sys.stdout.reconfigure(encoding='utf-8')


taille = 5

grille = [["🟩" for _ in range(taille)] for _ in range(taille)]
grille[2][2] = "🟥"

def afficher_grille(grille):
    for ligne in grille:
        print(" ".join(ligne))
    print("")
        
def a_un_voisin_1(grille, x, y):
    directions = [
        (-1, 0),  # haut
        (1, 0),   # bas
        (0, -1),  # gauche
        (0, 1)    # droite
    ]

    for dx, dy in directions:
        nx = x + dx
        ny = y + dy

        if 0 <= nx < taille and 0 <= ny < taille:
            if grille[nx][ny] == "🟥":
                return True

    return False

def propagation(grille):
    nouvelle_grille = [ligne.copy() for ligne in grille]

    for x in range(taille):
        for y in range(taille):
            if grille[x][y] == "🟩" and a_un_voisin_1(grille, x, y):
                nouvelle_grille[x][y] = "🟥"

    return nouvelle_grille


print("Grille initiale :")
afficher_grille(grille)
grille = propagation(grille)

print("Après 1 propagation :")
afficher_grille(grille)
grille = propagation(grille)
afficher_grille(grille)
grille = propagation(grille)
afficher_grille(grille)
grille = propagation(grille)
afficher_grille(grille)
 


#(0,0) (0,1) (0,2) (0,3) (0,4)

#(1,0) (1,1) (1,2) (1,3) (1,4)

#(2,0) (2,1) (2,2) (2,3) (2,4)

#(3,0) (3,1) (3,2) (3,3) (3,4)

#(4,0) (4,1) (4,2) (4,3) (4,4)
###  v1 de technique de verification des voisins
# def verifier_voisins(grille, x, y):
#     for i in range(max(0, x-1), min(taille, x+2)):
#         for j in range(max(0, y-1), min(taille, y+2)):
#             if (i, j) != (x, y) and grille[i][j] == "0":
#                 print(f"Verification de la cellule ({i},{j}) : {grille[i][j]}")
#             elif (i, j) != (x, y) and grille[i][j] == "1":
#                 print(f"Cellule infectée trouvée à ({i},{j})")
