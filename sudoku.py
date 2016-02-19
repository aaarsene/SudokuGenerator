#!/usr/bin/python3

from math import *
from random import *

TAILLE_GRILLE = 9
TAILLE_CARRE = int(sqrt(TAILLE_GRILLE))

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

def placement_possible(grille, chiffre, ligne, colone):
    if chiffre not in get_ligne(grille, ligne) \
        and chiffre not in get_colone(grille, colone) \
        and not in_carre(get_carre(grille, ligne, colone), chiffre):
        return True
    else:
        return False

def reinitialiser_depuis(grille, ligne, colone):
    for l in range(TAILLE_GRILLE):
        for c in range(TAILLE_GRILLE):
            if l > ligne:
                grille[l][c] = 0
            elif l == ligne and c >= colone:
                grille[l][c] = 0
    return grille

def remplir_grille(grille, history):
    deleted = False
    if len(history):
        if grille[history[-1][0]][history[-1][1]] == 0:
            deleted = True

    for ligne in range(TAILLE_GRILLE):
        for colone in range(TAILLE_GRILLE):
            case = grille[ligne][colone]
            if case == 0:
                possibles = []
                for chiffre in range(1,TAILLE_GRILLE+1):
                    if placement_possible(grille, chiffre, ligne, colone):
                        possibles.append(chiffre)
                if deleted:
                    possibles = history[-2][2]
                    possibles.pop(0)
                    history.pop()
                    deleted = False

                shuffle(possibles)
                if len(possibles):
                    grille[ligne][colone] = possibles[0]
                    history.append((ligne, colone, possibles))
                else:
                    return False
    return True

def get_back(history, grille):
    lastItem = len(history)
    for index in range(len(history)):
        if len(history[index][2]) > 1:
            lastItem = index

    grille = reinitialiser_depuis(grille, history[lastItem][0], history[lastItem][1])

    lastItem = lastItem + 1
    h = history[:lastItem]
    return h, grille

grille = [[0 for x in range(TAILLE_GRILLE)] for x in range(TAILLE_GRILLE)]

history = []
done = False

while in_carre(grille, 0) or not done:
    done = remplir_grille(grille, history)
    if not done:
        history, grille = get_back(history, grille)


affiche_grille(grille)
