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
        if self.__class__ == AbstractItemContent: raise RuntimeError("Can't instanciate abstract class AbstractItemContent directly.")
        super().__init__(master, **kwargs)
        # Note : self.master est une référence vers un cadre contenu dans AbstractMultiFrameItem ou GroupeAffichable
        self._schedulable = schedulable