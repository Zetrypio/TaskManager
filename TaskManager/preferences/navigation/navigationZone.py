# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk     import *
from tkinter import Label, Frame

from .selectionParametrage import *

class NavigationZone(Frame):
    def __init__(self, master = None, **kwargs):
        kwargs["bg"]= "white"
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est une référence vers FenetrePreferences

        self.selectionParamatrage = SelectionParametrage(self)
        self.selectionParamatrage.pack(side = LEFT, expand = YES, fill = BOTH)

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        return self.master.getApplication()

    def getFenetrePreferences(self):
        return self.master

    def getSelectionParamatrage(self):
        return self.selectionParamatrage

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def updateTreeview(self):
        self.getSelectionParamatrage().updateTreeview()
