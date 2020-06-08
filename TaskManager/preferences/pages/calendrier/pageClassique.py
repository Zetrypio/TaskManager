# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..AbstractPage import *

class PageClassique(AbstractPage):
    def __init__(self, master, **kwargs):
         # Note : self.master renvoie a ParametrageZone
        super().__init__(master,nom = "Classique", iid_parent ="-Calendrier", **kwargs)

        # Heure début + fin
        self.lbHeureDebut = Label(self._mFrame, text="Heure de début de journée par défaut :")
        self.sbHeureDebut = Spinbox(self._mFrame, from_=0, to=23, command=self.adaptSbHeureFin, width=5, format="%2.f:00")
        self.sbHeureDebut.set("8:00")
        self.lbHeureFin = Label(self._mFrame, text="Heure de fin de journée par défaut :")
        self.sbHeureFin = Spinbox(self._mFrame, from_=0, to=23, command=self.adaptSbHeureDebut, width=5, format="%2.f:59")
        self.sbHeureFin.set("18:59")
        self.adaptSbHeureDebut()
        self.adaptSbHeureFin()

        # Affichage
        self.lbHeureDebut.grid(column = 0, row = 0, sticky = "w")
        self.sbHeureDebut.grid(column = 1, row = 0, sticky = "e")
        self.lbHeureFin.grid(  column = 0, row = 1, sticky = "w")
        self.sbHeureFin.grid(  column = 1, row = 1, sticky = "e")

    def adaptSbHeureDebut(self):
        """
        Fonction qui adapte les possibilité du spinbox de l'heure de début en fonction de l'heure de fin
        """
        # Le split(":")[0] car il y a un certain formatage dans le spinbox
        self.sbHeureDebut.config(to=int(self.sbHeureFin.get().split(":")[0]))

    def adaptSbHeureFin(self):
        """
        Fonction qui adapte les possibilité du spinbox de l'heure de fin en fonction de l'heure de début
        """
        # Le split(":")[0] car il y a un certain formatage dans le spinbox
        self.sbHeureFin.config(from_=int(self.sbHeureDebut.get().split(":")[0]))

    def appliqueEffet(self, application):pass
