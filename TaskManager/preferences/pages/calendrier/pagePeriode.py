# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..AbstractPage import *

class PagePeriode(AbstractPage):
    def __init__(self, master, **kwargs):
         # Note : self.master renvoie a ParametrageZone
         # Note : Si on rajoute une option ne pas oublier d'ajouter la variable de contrôle à self._listData.append([variable, "texte explicatif", valeurParDéfaut])

        super().__init__(master,nom = "Période", iid_parent ="-Calendrier", **kwargs)

        # Choix du premier jour de la semaine pour le calendrier
        self.__labelComboSemaine = Label(self._mFrame, text="Premier jour de la semaine :")
        self.__varJour = StringVar()
        self._listData.append([self.__varJour, "Jour de début de semaine", "Lundi"])
        self.__comboJourSemaine = Combobox(self._mFrame, value=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"], state="readonly", textvariable = self.__varJour)

        # Affichage
        self.__labelComboSemaine.grid(column = 0, row = 0)
        self.__comboJourSemaine.grid(column = 1, row = 0, sticky = "NSEW")

        # Initialisation
        self._loadDataFile()

    def appliqueEffet(self, application):
        self._makeDictAndSave()
