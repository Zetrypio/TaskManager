# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from util.widgets.Dialog import *
from .navigation.navigationZone import *
from .parametrage.parametrageZone import *


# Pages
from .pages.pageGeneral import *
from .pages.general.pageClavier import *
from .pages.general.pageTheme import *

from .pages.pageCalendrier import *


class FenetrePreferences(Dialog):
    def __init__(self, application, master = None):
        super().__init__(master, title="Options", buttons = ('Ok', 'Appliquer', 'Annuler'), exitButton = ('Ok', 'Annuler', 'WM_DELETE_WINDOW'), command=self.valider)

        self.app = application

        # Initiallisation des frames et tout et tout
        self.navigationZone = NavigationZone(master = self)
        self.navigationZone.pack( side = LEFT, expand = NO, fill = BOTH, padx=2, pady=2)

        self.parametrageZone = ParametrageZone(master = self)
        self.parametrageZone.pack(side = LEFT, expand = YES, fill = BOTH, padx=2, pady=2)

        ## Gestion des pages
        self.listePage = []
        self.pageActive = None

        # Ajout des pages
        self.__ajouterPage(PageGeneral(self.getParametrageZone()))
        self.__ajouterPage(PageClavier(self.getParametrageZone()))
        self.__ajouterPage(PageTheme(self.getParametrageZone()))

        self.__ajouterPage(PageCalendrier(self.getParametrageZone()))

        # Initialisation de la page de garde
        self.setPageActive("-General")

    def __ajouterPage(self, Page):
        """
        Sert à rajouter une page dans le Treeview du navigationZone
        @param Page : <sous classe - AbstractPage> sous classe qui est à rajouter dans la liste
        """
        self.listePage.append(Page)
        self.updateTreeview()

    def setPageActive(self, iidPage):
        def pageByIdd(iid):
            """Retrouve la page lié à l'iid du Treeview"""
            return [page for page in self.listePage if page.getIid() == iidPage][0]

        # On supprime ce qu'il y a actuellement
        for page in self.listePage:
            page.pack_forget()

        # On fait une nouvelle page
        page = pageByIdd(iidPage)
        self.pageActive = page
        page.pack(side=LEFT, expand = YES, fill = BOTH)

    def updateTreeview(self):
        self.getNavigationZone().updateTreeview()

    def valider(self, txtBtn):
        if txtBtn == "Appliquer" or txtBtn == "Ok":
            for page in self.getListePage():
                page.appliqueEffet(self.getApplication())

    def getApplication(self):
        return self.app

    def getPageActive(self):
        return self.pageActive

    def getListePage(self):
        return self.listePage

    def getParametrageZone(self):
        return self.parametrageZone

    def getNavigationZone(self):
        return self.navigationZone

