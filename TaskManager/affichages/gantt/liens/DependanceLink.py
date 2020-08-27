# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.widgets.infobulle import *
from util.util import *

from .AbstractLink import *
from affichages.items.DatetimeItemPart import *

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
        #if partB.getSchedulable() in partA.getSchedulable().getDependantes():
            #raise RuntimeError("Lien déjà existant.")

        # Attributs :
        self.__objGantt_A = partA.getSchedulable()
        self.__objGantt_B = partB.getSchedulable()
        self.__selected = False

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def getPartObjA(self):
        """
        Getter pour le départ de la fleche
        @return <Task> self.__objGantt_A
        """
        return self.__objGantt_A

    def getPartObjB(self):
        """
        Getter pour l'arrivée de la fleche
        @return <Task> self.__objGantt_B
        """
        return self.__objGantt_B

    def isSelected(self):
        """
        Permet de savoir si le lien est sélectionné.
        """
        return self.__selected

    #############
    # Setters : #
    #############
    ""
    def setSelected(self, value):
        """
        Permet de changer l'état de sélection du lien.
        @param value: True si le lien doit être sélectionné, False sinon.
        """
        if not isinstance(value, bool):
            raise TypeError("Expected a boolean but got %s"%value)
        self.__selected = value
        self.highlight(color = None)
    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def highlight(self, color):
        """
        Permet de surligner ce lien d'une couleur donnée.
        @param color: la couleur à mettre.
        """
        if color is not None:
            super().highlight(color)
        elif self.__selected:
            super().highlight(self.getPalette()["selected"]) # old : "#0078FF"
        else:
            super().highlight(None)

    def inverserLaDependances(self):
        """
        Permet de changer le sens de la flèche.
        """
        # Attention, les attributs __objGanttA et __objGanttB sont pas des objetGantt mais des schedulables directement.
        self.__objGantt_B.removeDependance(self.__objGantt_A)
        self.__objGantt_A, self.__objGantt_B = self.__objGantt_B, self.__objGantt_A
        self.__objGantt_B.addDependance(self.__objGantt_A)
        # Update les parts aussi dans la superclasse
        self._updateParts(self.__objGantt_A.getLastPart(self._getAffichageGantt()), self.__objGantt_B.getFirstPart(self._getAffichageGantt()))

    def redraw(self, canvas, force = False):
        """
        Méthode pour dessiner la flèche.
        @param canvas: tkinter.Canvas() sur lequel dessiner la flèche du lien.
        """
        super().redraw(canvas, force)

        # Ajouter infobulle :
        ajouterInfoBulleTagCanvas(canvas, self.getTag(), "%s -> %s"%(self.getPartA().getSchedulable().getNom(), self.getPartB().getSchedulable().getNom()))

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def _onClic(self):
        self._getAffichageGantt().cancelEvent()
        self._getAffichageGantt().deselectEverything()
        self.__selected = True
        self._getAffichageGantt().getDonneeCalendrier().updateColor()
        #self._getAffichageGantt().clicSurObjet(self)

    def _onControlClic(self):
        self._getAffichageGantt().cancelEvent()
        self.__selected = not self.__selected
        self._getAffichageGantt().getDonneeCalendrier().updateColor()

    #def cliqueSuppr(self):
        #if self.tacheD.master.mode == "delDep":
            #if (chercheur := self.tacheD.master.getQuiCherche()) == None: # Objet TacheEnGantt qui a la variable jeCherche = True
                #self.tacheD.master.updateAffichage()
                #return
            #if chercheur != self.tacheD and chercheur != self.tacheF:
                #return
            #chercheur.jeCherche = False
            #self.suppression()

    #def changeSelect(self):
        #self.tacheD.master.updateAffichage()

    def delete(self):
        self.getPartB().getSchedulable().removeDependance(self.getPartA().getSchedulable())
