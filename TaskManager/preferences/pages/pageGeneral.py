# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label



from .AbstractPage import *


class PageGeneral(AbstractPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, nom = "General", **kwargs)
        # Note : self.master renvoie a ParametrageZone
        # Note : Si on rajoute une option, ne pas oublier d'ajouter la variable de contrôle à self._listData.append([variable, "texte explicatif", valeurParDefaut])
        # Note : Si l'option que l'on souhaite ajouter nécéssite un redémarrage pour s'appliquer, utiliser la méthode "self.__addDataNeedRestart(liste)", avec la même liste que pour self._listData

        ## LabelFrame Horloge
        self.__horlogeLabelFrame = LabelFrame(self._mFrame, text="Horloge")
        # widgets
        self.__varCaseTypeHorloge = BooleanVar()
        self._listData.append([self.__varCaseTypeHorloge, "Afficher les heures sur l'horloge", True])
        self.__caseTypeHorloge = Checkbutton(self.__horlogeLabelFrame, text = "Afficher les heures sur l'horloge lors de la sélection de la date d'une tache", variable=self.__varCaseTypeHorloge)


        # Affichage
        self.__horlogeLabelFrame.grid(column = 0, row = 0, sticky="NWES")
        self.__caseTypeHorloge.pack(side = TOP, expand = NO, fill = X)

        # Initialisation
        self._loadDataFile()

    "" # Marque pour le repli de code
    ###################################
    # Méthodes liées à la fermeture : #
    ###################################
    ""
    def appliqueEffet(self, application):
        self._makeDictAndSave()



