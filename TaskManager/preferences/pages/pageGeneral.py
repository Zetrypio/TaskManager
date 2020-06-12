# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showwarning
import os

from .AbstractPage import *


class PageGeneral(AbstractPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, nom = "General", **kwargs)
        # Note : self.master renvoie a ParametrageZone

        ## LabelFrame Horloge
        self.__horlogeLabelFrame = LabelFrame(self._mFrame, text="Horloge")
        # widgets
        self.__varCaseTypeHorloge = BooleanVar()
        self.__caseTypeHorloge = Checkbutton(self.__horlogeLabelFrame, text = "Afficher les heures sur l'horloge lors de la sélection de la date d'une tache", variable=self.__varCaseTypeHorloge)

        self.__lbPathCustomFile = Label(self._mFrame, text = "Chemin d'enregistrement de vos fichiers de préférences")
        self.__varEntryPath = StringVar()
        self.__entryPathCustomFile = Entry(self._mFrame, state="normal", textvariable = self.__varEntryPath)
        self.__btnParcourir = Button(self._mFrame, text = "...", command = self.__parcourir)



        # Affichage
        self.__horlogeLabelFrame.grid(column = 0, row = 0, sticky="NWES")
        self.__caseTypeHorloge.pack(side = TOP, expand = NO, fill = X)

        self.__lbPathCustomFile.grid(column = 0, row = 1, sticky = "w")
        self.__entryPathCustomFile.grid(column = 0, row = 2, sticky = "we")
        self.__btnParcourir.grid(column = 1, row = 2, sticky = "w")

    def __parcourir(self):
        """
        fonction qui demande où stocker les fichier ET vérifie si le dossier est bien vide
        """
        path = askdirectory(parent=self)
        # >= car il détect desktop.ini parfois ...
        while os.listdir(path):
            showwarning(title="Chemin invalide", message="Le dossier que vous avez choisi n'est pas valide")
            path = askdirectory(parent=self)
            if path == "":
                return
        self.__varEntryPath.set(path)

    def appliqueEffet(self, application):
        self.getData().setAffichageNombreHorloge(self.__varCaseTypeHorloge.get())



