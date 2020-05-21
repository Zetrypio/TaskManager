# -*- coding:utf-8 -*-
from .IDisplayableItem import *

# s
class AbstractMultiFrameItem(IDisplayableItem):
    """
    Classe représentant un item qui peut s'afficher dans
    un ou plusieurs cadre (Frame) de tkinter
    """
    def __init__(self, master, schedulable):
        if self.__class__ == AbstractMultiFrameItem: raise RuntimeError("Can't instanciate abtract class AbstractMultiFrameItem directly.")
        super().__init__()
        self.master = master
        self._listeCadre = []
        self._schedulable = schedulable
