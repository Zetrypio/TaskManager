# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

class AbstractItemContent(Frame):
    """
    Classe abstraite représentant le
    contenu d'un AbstractMultiFrameItem.
    """
    def __init__(self, master, schedulable, **kwargs):
        """
        Ne peut pas être instancié directement.
        Constructeur d'un contenu d'un AbstractMultiFrameItem().
        @param master: master du tkinter.Frame() que cet objet est.
        @param schedulable: l'AbstractSchedulableObject() considéré
        par cet objet.
        @param **kwargs: options à passer au constructeur parent,
        celui de tkinter.Frame() que cet objet est.
        """
        if self.__class__ == AbstractItemContent: raise RuntimeError("Can't instantiate abstract class AbstractItemContent directly.")
        super().__init__(master, **kwargs)
        # Note : self.master est une référence vers un cadre contenu dans AbstractMultiFrameItem ou GroupeAffichable
        self._schedulable = schedulable

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        return self._schedulable.getPeriode().getApplication()

    def getDonneeCalendrier(self):
        return self.getApplication().getDonneeCalendrier()

    def getSchedulable(self):
        """
        Getter du schedulable.
        @return le schedulable.
        """
        return self._schedulable

    def needButtonPlus(self, affichageGantt):
        """
        Permet de savoir si cette part à besoin d'un bouton
        plus à côté d'elle lors d'un affichage en Gantt.
        @return True si il y a besoin d'un bouton plus, False sinon.
        """
        raise NotImplementedError

    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def updateColor(self):
        """
        Permet de mettre à jour la couleur de l'objet, suivant sa sélection etc.
        """
        raise NotImplementedError

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def bindTo(self, binding, command, add=None):
        """
        Permet de binder un binding sur tout les sous-widget de ce widget,
        à redéfinir explicitement dans les sous-classes.
        Pour la documentation du binding, voir tkinter.Misc#bind(binding, command, add=None).
        Cependant, la commande prendra l'objet TODO
        """
        raise NotImplementedError
