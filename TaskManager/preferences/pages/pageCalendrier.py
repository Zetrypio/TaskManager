# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from .AbstractPage import *


class PageCalendrier(AbstractPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, nom = "Calendrier", **kwargs)
        # Note : self.master renvoie a ParametrageZone
        ## Widget
        self.__btnBackup = Button(self._mFrame, text = "Recharger les options des calendirer du dernier lancement ?", command = self.__backup)

        # Affichage
        self.__btnBackup.pack(side=TOP, fill=X)

    def __backup(self):
        """
        Fonction qui recharge les paramètre des calendrier lors du lancement
        A voir si on demande quel calendrier en particulier
        """
        pass

    def appliqueEffet(self, application):
        pass
