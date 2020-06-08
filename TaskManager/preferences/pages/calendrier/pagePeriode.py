# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..AbstractPage import *

class PagePeriode(AbstractPage):
    def __init__(self, master, **kwargs):
         # Note : self.master renvoie a ParametrageZone
        super().__init__(master,nom = "Période", iid_parent ="-Calendrier", **kwargs)

        # Choix du premier jour de la semaine pour le calendrier
        self.labelComboSemaine = Label(self._mFrame, text="Premier jour de la semaine :")
        self.comboJourSemaine = Combobox(self._mFrame, value=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"], state="readonly")
        self.comboJourSemaine.set("Lundi")

        # Affichage
        self.labelComboSemaine.grid(column = 0, row = 0)
        self.comboJourSemaine.grid(column = 1, row = 0, sticky = "NSEW")

    def appliqueEffet(self, application):pass
