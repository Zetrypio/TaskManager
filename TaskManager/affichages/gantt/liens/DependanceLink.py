# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.widgets.infobulle import *
from util.util import *

from .AbstractLink import *

class DependanceLink(AbstractLink):
    """
    Classe permettant de dessiner une flèche pour les dépendances,
    dans l'affichage Gantt.
    
    La flèche est soit courbée, si elle est sur un jour, en une forme ressemblant
    à une sorte de S en miroir, soit de manière sinusoïdale parcourant entre
    les tâches des jours entre le début et la fin.
    """
    def __init__(self, affichageGantt, partA, partB):
        """
        Constructeur du DependanceLink.

        @param affichageGantt: Référence vers l'affichageGantt pour avoir
        des informations sur le positionnement des parts.
        @param partA: DatetimeItemPart qui correspond au moment du début de la flèche.
        @param partB: DatetimeItemPart qui correspond au moment de la fin de la flèche.
        """
        # Constructeur parent :
        super().__init__(affichageGantt, partA, partB)

        # Tester si la dépendance existe déjà, si c'est vrai on ne le fait pas :
        if partB.getSchedulable() in partA.getSchedulable().getDependances():
            raise RuntimeError("Lien déjà existant.")

        # Attributs :
        self.__objGantt_A = partA.getSchedulable()
        self.__objGantt_B = partB.getSchedulable()
        self.__selected = False

        # Création de la dépendance :
        partB.getSchedulable().addDependance(partA.getSchedulable())

    def __setColor(self):
        # TODO : Couleur lors Ajout et Suppression.
        if self.__selected:
            self.setColor("#0078FF")
            self.setStrokeWeight(3)
        else:
            self.setColor("black")
            self.setStrokeWeight(2)

    def redraw(self, canvas):
        """
        Méthode pour dessiner la flèche.
        @param canvas: tkinter.Canvas() sur lequel dessiner la flèche du lien.
        """
        self.__setColor()
        super().redraw(canvas)

        # Ajouter infobulle :
        ajouterInfoBulleTagCanvas(canvas, self.getTag(), "%s -> %s"%(self.getPartA().getSchedulable().getNom(), self.getPartB().getSchedulable().getNom()))

    def _onClic(self):
        self._getAffichageGantt().cancelEvent()
        self._getAffichageGantt().deselectEverything()
        self.__selected = True
        self._getAffichageGantt().getDonneeCalendrier().updateColor()

    def _onControlClic(self):
        self._getAffichageGantt().cancelEvent()
        self.__selected = not self.__selected
        self._getAffichageGantt().getDonneeCalendrier().updateColor()

    def updateColor(self, canvas):
        self.__setColor()
        super().updateColor(canvas)

    def setSelected(self, value):
        """
        Permet de changer l'état de sélection du lien.
        @param value: True si le lien doit être sélectionné, False sinon.
        """
        if not isinstance(value, bool):
            raise TypeError("Expected a boolean but got %s"%value)
        self.__selected = value

#    def suppression(self):
#        self.tacheD.master.listeLien.remove(self)
#        self.tacheD.gestionRMenu()
#        self.tacheF.gestionRMenu() # Savoir si on supprime l'option retirer lien A mettre avant suppression car on prends en compte le lien actuel
#        self.tacheF.task.removeDependance(self.tacheD.task) # On retire la dépendance dans la tache
#        self.tacheD.master.updateAffichage()

    def inverserLaDependances(self):
        """
        Permet de changer le sens de la flèche.
        """
        if self.__objGantt_A.getSchedulable().getDebut() > self.__objGantt_B.getSchedulable().getDebut():
            self.__objGantt_B.getSchedulable().removeDependance(self.__objGantt_A.getSchedulable())
            self.__objGantt_A, self.__objGantt_B = self.__objGantt_B, self.__objGantt_A
            self.__objGantt_B.getSchedulable().addDependance(self.__objGantt_A.getSchedulable())

#    def cliqueSuppr(self):
#        if self.tacheD.master.mode == "delDep":
#            if (chercheur := self.tacheD.master.getQuiCherche()) == None: # Objet TacheEnGantt qui a la variable jeCherche = True
#                self.tacheD.master.updateAffichage()
#                return
#            if chercheur != self.tacheD and chercheur != self.tacheF:
#                return
#            chercheur.jeCherche = False
#            self.suppression()
#
#    def changeSelect(self):
#        self.select = not self.select
#        self.tacheD.master.updateAffichage()

