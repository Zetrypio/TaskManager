# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from .AbstractPage import *


class PageGeneral(AbstractPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, nom = "General", **kwargs)
        # Note : self.master renvoie a ParametrageZone

        ## LabelFrame Horloge
        self.__horlogeLabelFrame = LabelFrame(self, text="Horloge")
        # widgets
        self.__varCaseTypeHorloge = BooleanVar()
        self.__caseTypeHorloge = Checkbutton(self.__horlogeLabelFrame, text = "Afficher les heures sur l'horloge lors de la sélection de la date d'une tache", variable=self.__varCaseTypeHorloge)
        # Affichage
        self.__caseTypeHorloge.pack(  side = TOP, expand = NO, fill = X)
        self.__horlogeLabelFrame.pack(side = TOP, expand = NO, fill = X)

    def appliqueEffet(self, application):
        self.getApplication().getData().setAffichageNombreHorloge(self.__varCaseTypeHorloge.get())



