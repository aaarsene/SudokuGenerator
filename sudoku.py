#!/usr/bin/python3

from math import *
from random import *

TAILLE_GRILLE = 9
TAILLE_CARRE = int(sqrt(TAILLE_GRILLE))

tried = grille = [[[] for x in range(TAILLE_GRILLE)] for x in range(TAILLE_GRILLE)]

def get_colone(grille, index):
    coloneReturned = []
    for ligne in range(TAILLE_GRILLE):
        for colone in range(TAILLE_GRILLE):
            if colone == index:
                coloneReturned.append(grille[ligne][colone])
    return coloneReturned

def get_ligne(grille, index):
    return(grille[index])

def get_carre(grille, l, c):
    carre = [[0 for x in range(TAILLE_CARRE)] for x in range(TAILLE_CARRE)]
    carreX = 0
    carreY = 0

    for i in range(1,TAILLE_CARRE+1):
        if l < i*TAILLE_CARRE:
            carreY = i-1
            break

    for i in range(1,TAILLE_CARRE+1):
        if c < i*TAILLE_CARRE:
            carreX = i-1
            break

    for ligne in range(TAILLE_CARRE):
        for colone in range(TAILLE_CARRE):
            carre[ligne][colone] = grille[ligne+carreY*TAILLE_CARRE][colone+carreX*TAILLE_CARRE]

    return carre

def in_carre(carre, valeur):
    for ligne in carre:
        for case in ligne:
            if case == valeur:
                return True
    return False

def affiche_grille(grille):
    for ligne in range(TAILLE_GRILLE):
        for colone in range(TAILLE_GRILLE):
            print(grille[ligne][colone], end="")
            if colone in [2,5]:
                print("│", end="")
        print("")
        if ligne in [2,5]:
            print("───┼───┼───")
    print()

def remplir_grille(grille, history):
    ligneDebut = 0
    coloneDebut = 0
    deleted = False
    tailleHistorique = len(history)
    if len(history) and history[-1] == "Deleted":
        ligneDebut = history[-2][0]
        coloneDebut = history[-2][1]
        deleted = True

    for ligne in range(ligneDebut, TAILLE_GRILLE):
        for colone in range(coloneDebut, TAILLE_GRILLE):
            case = grille[ligne][colone]
            if case == 0:
                possibles = []
                for chiffre in range(1,TAILLE_GRILLE+1):
                    if chiffre not in get_ligne(grille, ligne) \
                        and chiffre not in get_colone(grille, colone) \
                        and not in_carre(get_carre(grille, ligne, colone), chiffre):
                        possibles.append(chiffre)
                if deleted:
                    if history[-2][2] not in tried[ligne][colone]:
                        tried[ligne][colone].append(history[-2][2])
                    for i in tried[ligne][colone]:
                        try:
                            possibles.remove(i)
                        except:
                            pass
                    history.pop()
                    history.pop()
                    deleted = False

                if len(possibles) > 1:
                    shuffle(possibles)
                    grille[ligne][colone] = possibles[0]
                    history.append((ligne, colone, grille[ligne][colone], True))
                elif len(possibles) == 1:
                    grille[ligne][colone] = possibles[0]
                    history.append((ligne, colone, grille[ligne][colone], False))
                else:
                    return False
    return True

def get_back(history, grille):
    lastItem = len(history)
    for index in range(len(history)):
        if history[index][3] == True:
            lastItem = index

    for item in history[lastItem:]:
        grille[item[0]][item[1]] = 0
    lastItem = lastItem + 1
    h = history[:lastItem]
    h.append("Deleted")
    return h, grille

grille = [[0 for x in range(TAILLE_GRILLE)] for x in range(TAILLE_GRILLE)]

history = []
done = False

while in_carre(grille, 0) or not done:
    done = remplir_grille(grille, history)
    if not done:
        history, grille = get_back(history, grille)


affiche_grille(grille)
