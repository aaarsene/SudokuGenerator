#!/usr/bin/python3

from math import *
from random import *

class Grille:
    def __init__(self, taille):
        self.taille_grille = taille
        self.taille_carre = int(sqrt(self.taille_grille))
        self.grille = [[0 for x in range(self.taille_grille)] for x in range(self.taille_grille)]
        self.history = []
        self.generer_grille()

    def get_colone(self, index):
        coloneReturned = []
        for ligne in range(self.taille_grille):
            for colone in range(self.taille_grille):
                if colone == index:
                    coloneReturned.append(self.grille[ligne][colone])
        return coloneReturned

    def get_ligne(self, index):
        return(self.grille[index])

    def get_carre(self, l, c):
        carre = [[0 for x in range(self.taille_carre)] for x in range(self.taille_carre)]
        carreX = 0
        carreY = 0

        for i in range(1,self.taille_carre+1):
            if l < i*self.taille_carre:
                carreY = i-1
                break

        for i in range(1,self.taille_carre+1):
            if c < i*self.taille_carre:
                carreX = i-1
                break

        for ligne in range(self.taille_carre):
            for colone in range(self.taille_carre):
                carre[ligne][colone] = self.grille[ligne+carreY*self.taille_carre][colone+carreX*self.taille_carre]

        return carre

    def in_carre(self, carre, valeur):
        for ligne in carre:
            for case in ligne:
                if case == valeur:
                    return True
        return False

    def zeros(self):
        if self.in_carre(self.grille, 0):
            return True
        else:
            return False

    def get_string(self):
        result = ""
        for ligne in range(self.taille_grille):
            for colone in range(self.taille_grille):
                result = result + "{}".format(self.grille[ligne][colone])
                if colone in range(self.taille_carre-1,self.taille_grille-1,self.taille_carre):
                   result = result + "|"
            result = result + "\n"
            if ligne in range(self.taille_carre-1,self.taille_grille-1,self.taille_carre):
                for colone in range(self.taille_grille):
                    result = result + "-"
                    if colone in range(self.taille_carre-1,self.taille_grille-1,self.taille_carre):
                        result = result + "+"
                result = result + "\n"
        return result

    def affiche_grille(self):
        print(self.get_string())

    def placement_possible(self, chiffre, ligne, colone):
        if chiffre not in self.get_ligne(ligne) \
            and chiffre not in self.get_colone(colone) \
            and not self.in_carre(self.get_carre(ligne, colone), chiffre):
            return True
        else:
            return False

    def reinitialiser_depuis(self, ligne, colone):
        for l in range(self.taille_grille):
            for c in range(self.taille_grille):
                if l > ligne:
                    self.grille[l][c] = 0
                elif l == ligne and c >= colone:
                    self.grille[l][c] = 0

    def remplir_grille(self):
        deleted = False
        if len(self.history):
            if self.grille[self.history[-1][0]][self.history[-1][1]] == 0:
                deleted = True

        for ligne in range(self.taille_grille):
            for colone in range(self.taille_grille):
                case = self.grille[ligne][colone]
                if case == 0:
                    possibles = []
                    for chiffre in range(1,self.taille_grille+1):
                        if self.placement_possible(chiffre, ligne, colone):
                            possibles.append(chiffre)
                    if deleted:
                        possibles = self.history[-2][2]
                        possibles.pop(0)
                        self.history.pop()
                        deleted = False

                    shuffle(possibles)
                    if len(possibles):
                        self.grille[ligne][colone] = possibles[0]
                        self.history.append((ligne, colone, possibles))
                    else:
                        return False
        return True

    def get_back(self):
        lastItem = len(self.history)
        for index in range(len(self.history)):
            if len(self.history[index][2]) > 1:
                lastItem = index

        self.reinitialiser_depuis(self.history[lastItem][0], self.history[lastItem][1])

        lastItem = lastItem + 1
        self.history = self.history[:lastItem]

    def generer_grille(self):
        while self.zeros():
            self.remplir_grille()
            if self.zeros():
                self.get_back()


if __name__ == '__main__':
    g = Grille(9)
    g.affiche_grille()
