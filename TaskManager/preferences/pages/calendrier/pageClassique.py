# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..AbstractPage import *

class PageClassique(AbstractPage):
    def __init__(self, master, **kwargs):
         # Note : self.__master renvoie a ParametrageZone
         # Note : Si on rajoute une option ne pas oublier d'ajouter la variable de controle à self._listData.append([variable, "texte explicatif", variableParDefaut])

        super().__init__(master,nom = "Classique", iid_parent ="-Calendrier", **kwargs)

        # Heure début + fin
        self.__lbHeureDebut = Label(self._mFrame, text="Heure de début de journée par défaut :")
        self.__varHeureDebut = StringVar()
        self._listData.append([self.__varHeureDebut, "Heure de début", "8:00"])
        self.__sbHeureDebut = Spinbox(self._mFrame, from_=0, to=23, command=self.__adaptSbHeureFin, width=5, format="%2.f:00", textvariable = self.__varHeureDebut)
        self.__lbHeureFin = Label(self._mFrame, text="Heure de fin de journée par défaut :")
        self.__varHeureFin = StringVar()
        self._listData.append([self.__varHeureFin, "Heure de fin", "18:59"])
        self.__sbHeureFin = Spinbox(self._mFrame, from_=0, to=23, command=self.__adaptSbHeureDebut, width=5, format="%2.f:59", textvariable = self.__varHeureFin)

        # Affichage
        self.__lbHeureDebut.grid(column = 0, row = 0, sticky = "w")
        self.__sbHeureDebut.grid(column = 1, row = 0, sticky = "e")
        self.__lbHeureFin.grid(  column = 0, row = 1, sticky = "w")
        self.__sbHeureFin.grid(  column = 1, row = 1, sticky = "e")

        # Initialisation
        self._loadDataFile()
        self.__adaptSbHeureDebut()
        self.__adaptSbHeureFin()

    def __adaptSbHeureDebut(self):
        """
        Fonction qui adapte les possibilité du spinbox de l'heure de début en fonction de l'heure de fin
        """
        # Le split(":")[0] car il y a un certain formatage dans le spinbox
        self.__sbHeureDebut.config(to=int(self.__varHeureFin.get().split(":")[0]))

    def __adaptSbHeureFin(self):
        """
        Fonction qui adapte les possibilité du spinbox de l'heure de fin en fonction de l'heure de début
        """
        # Le split(":")[0] car il y a un certain formatage dans le spinbox
        self.__sbHeureFin.config(from_=int(self.__varHeureDebut.get().split(":")[0]))

    def appliqueEffet(self, application):
        self._makeDictAndSave()
