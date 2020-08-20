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
        # Note : Si l'option que l'on souhaite ajouter nécéssite un redémarrage pour s'appliquer, utiliser la méthode "self._addDataNeedRestart(liste)", avec la même liste que pour self._listData

        ## Variable
        self.__varCaseTypeHorloge = BooleanVar()
        self._listData.append([self.__varCaseTypeHorloge, "Afficher les heures sur l'horloge", True])
        self.__varChargerLastPeriode = BooleanVar()
        self._addDataNeedRestart([self.__varChargerLastPeriode, "charger dernière période", False])
        self.__varAllowAutoSave = BooleanVar()
        self._addDataNeedRestart([self.__varAllowAutoSave, "auto-save", True])
        self.__varNbAutoSave = StringVar()
        self._listData.append([self.__varNbAutoSave, "intervalle auto-save", 5])
        self.__varAllowAutoDelete = BooleanVar()
        self._listData.append([self.__varAllowAutoDelete, "auto-delete", True])
        self.__varNbAutoDelete = StringVar()
        self._listData.append([self.__varNbAutoDelete, "duree auto-delete", 3])
        self.__varUnitAutoDelete = StringVar()
        self._listData.append([self.__varUnitAutoDelete, "unité de l'auto del", "mois"])

        ## LabelFrame Horloge
        self.__horlogeLabelFrame = LabelFrame(self._mFrame, text="Horloge")
        # widgets
        self.__caseTypeHorloge = Checkbutton(self.__horlogeLabelFrame, text = "Afficher les heures sur l'horloge lors de la sélection de la date d'une tache", variable=self.__varCaseTypeHorloge)
        ## LabelFrame Sauvegarde & Chargement
        self.__saveAndLoad = LabelFrame(self._mFrame, text = "Chargement et sauvegarde")
        self.__caseChargerPeriode = Checkbutton(self.__saveAndLoad, text = "Charger la dernière période utilisé", variable = self.__varChargerLastPeriode)
        self.__caseAllowAutoSave = Checkbutton(self.__saveAndLoad, text = "Sauvegarde automatique", variable = self.__varAllowAutoSave, command = self.__allowChangeAutosave)
        self.__sbIntervalle = Spinbox(self.__saveAndLoad, from_ = 1, to = 100, textvariable = self.__varNbAutoSave)
        self.__cbUnitAutoSave = Label(self.__saveAndLoad, text = "minutes")
        self.__caseAllowAutoDelete = Checkbutton(self.__saveAndLoad, text = "Suppression automatique", variable = self.__varAllowAutoDelete, command = self.__allowChangeAutoDelete)
        self.__sbIntervalleDel = Spinbox(self.__saveAndLoad, from_ = 0, to = 100, textvariable = self.__varNbAutoDelete)
        self.__cbUnitAutoSaveDel = Combobox(self.__saveAndLoad, value = ["mois", "semaines", "jours"], textvariable = self.__varUnitAutoDelete)


        ## Affichage
        self.__horlogeLabelFrame.grid(  row = 0, column = 0, sticky="NWES")
        self.__caseTypeHorloge.pack(    side = TOP, expand = NO, fill = X)
        self.__saveAndLoad.grid(        row = 1, column = 0)

        self.__caseChargerPeriode.grid( row = 0, column = 0, sticky = "nsew")
        self.__caseAllowAutoSave.grid(  row = 1, column = 0, sticky = "we")
        self.__sbIntervalle.grid(       row = 1, column = 1)
        self.__cbUnitAutoSave.grid(     row = 1, column = 2)
        self.__caseAllowAutoDelete.grid(row = 2, column = 0, sticky = "we")
        self.__sbIntervalleDel.grid(    row = 2, column = 1)
        self.__cbUnitAutoSaveDel.grid(  row = 2, column = 2)

        # Initialisation
        self._loadDataFile()
        self.__allowChangeAutosave()
        self.__allowChangeAutoDelete()

    "" # Marque pour le repli de code
    ##############
    # Méthodes : #
    ##############
    ""
    def __allowChangeAutoDelete(self):
        """
        Méthode qui gère l'état des widget de l'intervelle de l'autoSave
        """
        mode = "normal" if self.__varAllowAutoDelete.get() else "disabled"
        self.__sbIntervalleDel.config( state = mode)
        self.__cbUnitAutoSaveDel.config(state = mode)

    def __allowChangeAutosave(self):
        """
        Méthode qui gère l'état des widget de l'intervelle de l'autoSave
        """
        mode = "normal" if self.__varAllowAutoSave.get() else "disabled"
        self.__sbIntervalle.config( state = mode)
        self.__cbUnitAutoSave.config(state = mode)

    ""
    ###################################
    # Méthodes liées à la fermeture : #
    ###################################
    ""
    def appliqueEffet(self, application):
        self._makeDictAndSave()



