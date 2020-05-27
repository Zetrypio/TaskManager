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
        Constructeur d'un contenu d'un AbstractMultiFrameItem.
        @param master: master du Frame que cet objet est.
        @param schedulable: l'AbstractSchedulableObject considéré
        par cet objet.
        @param **kwargs: options à passer au constructeur parent,
        celui de tkinter.Frame().
        """
        if self.__class__ == AbstractItemContent: raise RuntimeError("Can't instanciate abstract class AbstractItemContent directly.")
        super().__init__(master, **kwargs)
        # Note : self.master est une référence vers un cadre contenu dans AbstractMultiFrameItem ou GroupeAffichable
        self._schedulable = schedulable