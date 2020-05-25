# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from util.widgets.Dialog import *
from .navigation.navigationZone import *
from .parametrage.parametrageZone import *

class FenetrePreferences(Dialog):
    def __init__(self, application, master = None):
        super().__init__(master, title="Options", buttons = ('Ok', 'Appliquer', 'Annuler'), exitButton = ('Ok', 'Annuler', 'WM_DELETE_WINDOW'), command=self.valider)

        self.app = application

        # Initiallisation des frames et tout et tout
        self.navigationZone = NavigationZone(master = self)
        self.navigationZone.pack( side = LEFT, expand = NO, fill = BOTH, padx=2, pady=2)

        self.parametrageZone = ParametrageZone(master = self)
        self.parametrageZone.pack(side = LEFT, expand = YES, fill = BOTH, padx=2, pady=2)

        # Gestion des pages
        self.listePage = []

    def __ajouterPage(self, Page):
        """
        Sert à rajouter une page dans le Treeview du navigationZone
        @param Page : <sous classe - AbstractPage> sous classe qui est à rajouter dans la liste
        """
        self.listePage.append(Page)
        self.updateTreeview()

    def updateTreeview(self):
        self.getNavigationZone().updateTreeview()

    def valider(self, txtBtn):pass

    def getApp(self):
        return self.app

    def getListePage(self):
        return self.listePage

    def getParametrageZone(self):
        return self.parametrageZone

    def getNavigationZone(self):
        return self.navigationZone

