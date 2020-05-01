# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.widgets.infobulle import *
from util.util import *

class LienDependance: # Classe qui gère toutes les dépendances niveau visuel
    def __init__(self, tacheDebut, tacheFin, canvas):
        self.tacheD = tacheDebut # Où part   le lien | TacheEnGantt
        self.tacheF = tacheFin #   Où arrive le lien | TacheEnGantt
        
        for tache in self.tacheD.task.dependances: # Tester si la dépendance existe déjà, si c'est vrai on ne le fait pas
            if self.tacheF.task == tache:
                raise ValueError("Lien déjà existant.")

        self.chemin = [] # Chemin que va suivre le lien pour la gestion de l'affichage
        
        self.ID_LIEN = None

        self.canvas = canvas
        self.select = False # variable qui sait si on est selectionne ou pas

        self.tacheF.task.addDependance(self.tacheD.task) # On créer la dépendance dans la tache

    def suppression(self):
        self.tacheD.master.listeLien.remove(self)
        self.tacheD.gestionRMenu()
        self.tacheF.gestionRMenu() # Savvoir si on supprime l'option retirer lien A mettre avant suppresssion car on prends en compte le lien actuel
        self.tacheF.task.removeDependance(self.tacheD.task) # On retire la dépendance dans la tache
        self.tacheD.master.updateAffichage()

    def inverserLaDependances(self):
        """
        Permet de changer le sens de la flèche
        """
        self.tacheF.task.removeDependance(self.tacheD.task)
        self.tacheD, self.tacheF = self.tacheF, self.tacheD
        self.tacheF.task.addDependance(self.tacheD.task)
        
    def afficherLesLiens(self, couleur = "#000000"):
        from .AffichageGantt import AffichageGantt # Pour éviter les imports circulaires
        # On ne fait pas si on est pas dans la periode a afficher
        if (self.tacheD.task.debut.date() == self.tacheF.task.debut.date() and (self.tacheF.task.getFin().date() < self.tacheD.master.getJourDebut() or self.tacheD.task.getFin().date() >= self.tacheD.master.getJourFin())) \
        or (self.tacheD.task.debut.date() != self.tacheF.task.debut.date() and (self.tacheF.task.getFin().date() <= self.tacheD.master.getJourDebut() or self.tacheD.task.debut.date() > self.tacheD.master.getJourFin())):
            return
        

        self.pathCalculing() # On calcul le nouveau chemin

        # Gestion des couleurs
        w = 2
        if self.tacheD.jeCherche == True or self.tacheF.jeCherche == True: # Change la couleur si on séléctionne une tache pour une action
            couleur = "#FFAF00"
            if self.tacheD.master.mode == "delDep":
                couleur = "#FF3F3F"
            w = 3
        elif self.select == True:
            couleur = "#0078FF"
            w = 3

        # Paramètre généraux
        tailleLigne   = AffichageGantt.TAILLE_LIGNE
        tailleColonne = self.tacheD.master.tailleColonne
        facteurW      = self.tacheD.master.facteurW

        temp = self.tacheD.getPosPixel()
        if temp != None:
            x1D, y1D, x2D, y2D = temp
        else:
            x1D = x2D = 0
            y1D = self.tacheD.getPosGrille()[2]*tailleLigne
            y2D = y1D+tailleLigne-4

        heightD = y2D-y1D
        

        temp = self.tacheF.getPosPixel()
        if temp != None:
            x1F, y1F, x2F, y2F = temp
        else:
            # y1F et 2 avec chemin
            if self.tacheF.task.debut.date() == self.canvas.master.getJourFin():
                x1F = self.canvas.winfo_width()
                for val in self.chemin:
                    if val != -1:
                        y1F = val*tailleLigne+13
                        y2F = y1F+tailleLigne-4+13
            else:
                x1F = self.canvas.winfo_width()+50 # + 50 Pour faire sortir la flèche du cadre
                for val in self.chemin:
                    if val != -1:
                        y1F = val*tailleLigne+20
                        y2F = y1F-AffichageGantt.ESPACEMENT

        heightF = y2F-y1F

        self.ID_LIEN = tag = "lienum"+str(self.tacheD.master.listeLien.index(self))

        if w == 3:
            tag = (tag, "top", "lienDep")
        else :
            tag = (tag, "lienDep")

        if x1F < x2D: # Si la tache et son lien sont le même jour
            rayon = tailleLigne/4
            self.canvas.create_arc(x2D-rayon, 13+y1D+heightD/2-rayon, x2D+rayon, 13+y1D+heightD/2+rayon, start=-90, extent=180, style='arc', width=w,  outline=couleur, tags=tag)
            self.canvas.create_line(x2D+1, y2D+3, x1D-10, y2D+3, width=w, fill=couleur, smooth=1, tags=tag)
            self.canvas.create_arc(x1D-rayon-10,y1D+tailleLigne-rayon+12, x1D+rayon-10,y1D+tailleLigne+rayon+12,  start=90, extent=90, style='arc', width=w, outline=couleur, tags=tag)

            self.canvas.create_line(x1D-rayon-10,y1D+tailleLigne+rayon-1, x1D-rayon-10, y1F+rayon , width=w, fill=couleur, smooth=1, tags=tag)

            self.canvas.create_arc(x1F-rayon-10, y1F+heightF/2-2*rayon, x1F+rayon-10, y1F+heightF/2, start=180, extent=90, style='arc', width=w, outline=couleur, tags=tag)
            self.canvas.create_line(x1F-10, y1F+heightF/2, x1F, y1F+heightF/2, width=w, fill=couleur, arrow=LAST, smooth=1, tags=tag)

        else:
            mesPoints = []
            def dessineLiaison(x1, y1, x2, y2):
                  for x in range(int(x1), int(x2)+1):
                    y = posY(x, x1, y1, x2, y2)
                    mesPoints.append([x, y])

            # S'il n'y a qu'un jour de décalage entre la fin du début et le début de la fin
            if self.tacheD.task.getFin().date() == (self.tacheF.task.getDebut() - datetime.timedelta(days=1)).date():
#                 On dessine autrement
                dessineLiaison(x2D,
                               y1D+heightD/2,
                               x1F-10,
                               y1F+heightF/2)
#                self.canvas.create_line(x2D, y1D+heightD/2, x1F+tailleColonne*(1-facteurW), y1F+(y1F+y2F)/2)
            else : # Si c'est classique
                dessineLiaison(x2D,
                               y1D+heightD/2,
                               x2D+tailleColonne*(1-facteurW),
                               max(tailleLigne*self.chemin[(self.tacheD.task.getFin()).isoweekday()]+AffichageGantt.TAILLE_BANDEAU_JOUR - AffichageGantt.ESPACEMENT/2, AffichageGantt.TAILLE_BANDEAU_JOUR))

            # Si la fin de la tache d'arrivé est avant la fin de l'affichage ET la tache de fin n'est pas un jour après
            if self.tacheD.master.getJourFin() >= self.tacheF.task.debut.date() and self.tacheD.task.getFin().date() != (self.tacheF.task.getDebut() - datetime.timedelta(days=1)).date():
                dessineLiaison(x1F-tailleColonne*(1-facteurW),
                               max(tailleLigne*self.chemin[(self.tacheD.task.getFin()).isoweekday()]+AffichageGantt.TAILLE_BANDEAU_JOUR - AffichageGantt.ESPACEMENT/2, AffichageGantt.TAILLE_BANDEAU_JOUR),
                               x1F-10,
                               max(y1F+heightF/2, 20))

            # Fin droite pour une foli flèche
            mesPoints.append([x1F, max(y1F+heightF/2, 20)])

            self.canvas.create_line(*mesPoints, width=w, arrow=LAST, fill=couleur, smooth=1, tags=tag)

        # On ajoute une infobulle :
        ajouterInfoBulleTagCanvas(self.canvas, tag, self.tacheD.task.nom+"→"+self.tacheF.task.nom) # flèche trop cool en attende "→"

    def pathCalculing(self):
        " Fonction qui permet de calculer le chemin que va prendre le lien pour lier les 2 taches "
        self.chemin = [] # On réinitialise le parcours

        _, posXD, posYD = self.tacheD.getPosGrille()
        _, posXF, posYF = self.tacheF.getPosGrille()

        croissance = posYF-posYD # savoir si on descend ou si on monte (c'est à l'envers les axes

        for jour in range(self.canvas.master.getLongueurPeriode()): # et on recalcule
            if posXD == jour and posXF == jour: # Si la tacheD est le même jour que TacheF
                self.chemin.append(1+posYD)
            elif posXD < jour and posXF > jour:
                self.chemin.append(posYD+croissance)
            else:
                self.chemin.append(-1)

    def cliqueSuppr(self):
        if self.tacheD.master.mode == "delDep":
            if (chercheur := self.tacheD.master.getQuiCherche()) == None: # Objet TacheEnGantt qui a la variable jeCherche = True
                self.tacheD.master.updateAffichage()
                return
            if chercheur != self.tacheD and chercheur != self.tacheF:
                return
            chercheur.jeCherche = False
            self.suppression()

    def changeSelect(self):
        self.select = not self.select
        self.tacheD.master.updateAffichage()

