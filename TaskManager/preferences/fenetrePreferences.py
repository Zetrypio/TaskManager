# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from util.widgets.Dialog import *
from .navigation.navigationZone import *
from .parametrage.parametrageZone import *
from .dialog.askRestart import *

# Pages
from .pages.pageGeneral import *
from .pages.general.pageClavier import *
from .pages.general.pageProfil import *
from .pages.general.pageTheme import *

from .pages.pageCalendrier import *
from .pages.calendrier.pageClassique import *
from .pages.calendrier.pageGantt import *
from .pages.calendrier.pagePeriode import *


class FenetrePreferences(Dialog):
    def __init__(self, application, master = None):
        super().__init__(master, title="Options", buttons = ('Ok', 'Appliquer', 'Annuler'), exitButton = ('Ok', 'Annuler', 'WM_DELETE_WINDOW'), command=self.valider)

        self.app = application

        # Initialisation des frames et tout et tout
        self.navigationZone = NavigationZone(master = self)
        self.navigationZone.pack( side = LEFT, expand = NO, fill = BOTH, padx=2, pady=2)

        self.parametrageZone = ParametrageZone(master = self)
        self.parametrageZone.pack(side = LEFT, expand = YES, fill = BOTH, padx=2, pady=2)

        # Variable pour indiquer si on doit restart
        self.mustRestart = False

        # Gestion des pages
        self.listePage = []
        self.pageActive = None

        # Ajout des pages
        self.__ajouterPage(PageGeneral(self.getParametrageZone()))
        self.__ajouterPage(PageClavier(self.getParametrageZone()))
        self.__ajouterPage(PageProfil(self.getParametrageZone()))
        self.__ajouterPage(PageTheme(self.getParametrageZone()))

        self.__ajouterPage(PageCalendrier(self.getParametrageZone()))
        self.__ajouterPage(PageClassique(self.getParametrageZone()))
        self.__ajouterPage(PageGantt(self.getParametrageZone()))
        self.__ajouterPage(PagePeriode(self.getParametrageZone()))


        # Pour que la page profil soit la dernière a être activé lorsqu'on fais appliqueEffet
        # Comme ça chacun enregistre ses choix dans son fichier
        # À la fin, on déplace les fichier si jamais on choisis de changer
        for page in self.listePage:
            if isinstance(page, PageProfil):
                self.listePage.append(self.listePage.pop(self.listePage.index(page)))

        # Initialisation de la page de garde
        self.setPageActive("-General")

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        """ return self.app """
        return self.app

    def getListePage(self):
        return self.listePage

    def getNavigationZone(self):
        return self.navigationZone

    def getPageActive(self):
        return self.pageActive

    def getParametrageZone(self):
        return self.parametrageZone

    def getRestartMode(self):
        """
        Getter du mode pour restart
        @return self.mustRestart : <bool> True si il faut redemarrer
                                          False si pas besoin
        """
        return self.mustRestart

    ""
    #############
    # Setters : #
    #############
    ""
    def setPageActive(self, iidPage):
        """
        @param iidPage : <str> contient l'iid de la page à mettre en premier plan
            construction de l'iid : "-" + nomDeLaPageParent   | + "-" + nomDeLaPageParent |*nb de page au dessus
        """
        def pageByIdd(iid):
            """
            Retrouve la page lié à l'iid du Treeview
            + si erreur on retourne la page sur laquelle on est
            """
            for page in self.listePage:
                if page.getIid() == iidPage:
                    return page
            else:
                return self.getPageActive()

        # On supprime ce qu'il y a actuellement
        for page in self.listePage:
            page.pack_forget()

        # On fait une nouvelle page
        page = pageByIdd(iidPage)
        self.pageActive = page
        page.pack(side=LEFT, expand = YES, fill = BOTH)

    def setRestartMode(self):
        """
        Permet de dire qu'il faudra relancer l'application
        S'occupe seulement de mettre en True
        """
        self.mustRestart = True

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def __ajouterPage(self, Page):
        """
        Sert à rajouter une page dans le Treeview du navigationZone
        @param Page : <sous classe - AbstractPage> sous classe qui est à rajouter dans la liste
        """
        self.listePage.append(Page)
        self.updateTreeview()

    def updateTreeview(self):
        self.getNavigationZone().updateTreeview()

    def valider(self, txtBtn):
        """
        Permet de sauvegarder tout ce qui doit être sauvegarder sur chaque page
        """
        if txtBtn == "Appliquer" or txtBtn == "Ok":
            for page in self.getListePage():
                page.appliqueEffet(self.getApplication())
                # Doit-on restart l'application ?
                if self.getRestartMode():
                    self.mustRestart = False
                    if askRestart():
                        self.getApplication().restart()

            # Et on update Affichage
            self.getApplication().getDonneeCalendrier().updateAffichage()
            self.getApplication().getTaskEditor().redessiner()
