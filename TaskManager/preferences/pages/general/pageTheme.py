# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.colorchooser import askcolor
import tkinter.messagebox

from preferences.themes.themeLoader import *
from ..AbstractPage import *
from util.widgets.ColorButton import *
from util.widgets.Dialog import askstring, askyesnowarning

"""
{"Name" : nomTheme,
            "Couleur principale": self.__lbColor1.cget("text") or "#ffffff",
            "Couleur secondaire": self.__lbColor2.cget("text") or "#ffffff",
            "Couleur tertiaire" : self.__lbColor3.cget("text") or "#ffffff",
            "# Couleur par élément" : "",
            "General-Couleur du texte" : self.__varGCDT or "Couleur principale",
            "Liste des tâches-Couleur de fond" : self.__varLDTCDF or "Couleur principale",
            "Ajout des tâches-Couleur de fond" : self.__varADTCDF or "Couleur principale",
            "Zone des onglets-Couleur de fond" : self.__varZDOCDF or "Couleur principale",
            "Zone des onglets-Couleur de fond du calendrier" : self.__varZDOCDFDC or "Couleur principale",
            "Zone des onglets-Couleur de fond de l'affichage Gantt" : self.__varZDOCDFDAG or "Couleur principale",
            "Zone des onglets-Couleur de fond de l'affichage des périodes" : self.__varZDOCDFDADP or "Couleur principale",
            "Zone des onglets-Couleur de fond de l'affichage des tâches suivantes" : self.__varZDOCDFDADTS or "Couleur principale",
            "Zone de l'affichage-Couleur de fond" : self.__varZDACDF or "Couleur principale",
            "Barre d'outils principale-Couleur de fond" : self.__varBOPCDF or "Couleur principale",
            "Barre d'outils principale-Couleur des boutons" : self.__varBOPCDB or "Couleur principale",
            "Barre d'outils secondaire-Couleur de fond" : self.__varBOSCDF or "Couleur principale",
            "Barre d'outils secondaire-Couleur des boutons" : self.__varBOSCDB or "Couleur principale",
            "# Autre que les couleurs" : "",
            "Boutons de ttk" : self.__varTtkButton.get()}
"""

NOMFICHIER = os.sep + "theme"


class PageTheme(AbstractPage):
    def __init__(self, master, **kwargs):
         # Note : self.master renvoie a ParametrageZone
         # Note : Si on rajoute une option, ne pas oublier d'ajouter la variable de contrôle à self._listData.append([variable, "texte explicatif", valeurParDefaut])
         # Note : Si l'option que l'on souhaite ajouter nécéssite un redémarrage pour s'appliquer, utiliser la méthode "self.__addDataNeedRestart(liste)", avec la même liste que pour self._listData

        super().__init__(master, nom = "Thème", iid_parent ="-General", **kwargs)

        # Traitement du fichier .ini
        # self.getData() = ConfigParser()
        self.readFile(NOMFICHIER) # Prise de conscience de ce qu'il y a dedans


        self.__currentElem = None # iid de l'élément sélectionné dans le TreeView

        self.__listeVarTheme = ["nom"]


        self.__varAdapteTexteTache = BooleanVar()
        self._listData.append([self.__varAdapteTexteTache, "Couleur adaptative", False])
        self.__caseAdaptTexteTache = Checkbutton(self._mFrame, text="Changer la couleur du texte d'une tache (noir/blanc) en fonction de la couleur de fond de la tache", variable=self.__varAdapteTexteTache)

        # COMBO THEME
        self.__varTheme = StringVar()
        self._listData.append([self.__varTheme, "theme", "default"])
        self.__cbRealTheme = Combobox(self._mFrame, value = getThemes(), textvariable = self.__varTheme)
        self.__cbRealTheme.bind("<<ComboboxSelected>>", lambda e = None : self.prevent())
        # Text mettant en garde sur l'utilisation de certains thèmes
        self.__varPerf = StringVar()
        self.__lbPerf = Label(self._mFrame, textvariable = self.__varPerf, anchor = W)


        ## Affichage
        self.__caseAdaptTexteTache.grid(row = 0, column = 0, columnspan = 2)
        Label(self._mFrame, text = "Thème :").grid(row = 1, column = 0)
        self.__cbRealTheme.grid(row = 1, column = 1, sticky = "we")
        self.__lbPerf.grid(row = 2, column = 0, sticky = "w")


        # Final
        self._loadDataFile() # Pour les prefs standards
        themeUse(self.tk, self.__varTheme.get(), self, self.getApplication())

    ""
    #############
    # Setters : #
    #############
    ""
    def prevent(self):
        """
        Méthode qui gère le label sur les performances en fonction des thèmes
        """
        if self.__varTheme.get() == "equilux":
            self.__varPerf.set("Ce thème affecte grandement les performance de l'application")
        elif "scid" in self.__varTheme.get():
            self.__varPerf.set("Ce thème affecte les performance de l'application")
        elif self.__varTheme.get() == "aquativo":
            self.__varPerf.set("Ce thème affecte légèrement les performance de l'application")
        else :
            self.__varPerf.set("")

    def appliqueEffet(self, application):
        # Si on a changé le thème
        if self.getData().dataExist("General", "Thème", "theme") and self.__varTheme.get() != self.getData().getOneValue("General", "Thème", "theme"):
            themeUse(self.tk, self.__varTheme.get(), self, self.getApplication())

        self._makeDictAndSave()
