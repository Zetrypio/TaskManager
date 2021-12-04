# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.messagebox import showerror
from shutil import move
import os

from ..AbstractPage import *
from util.widgets.Dialog import askyesnowarning

from ...dialog.askFolder import *


class PageProfil(AbstractPage):
    def __init__(self, master, **kwargs):
        # Note : self.master renvoie a ParametrageZone
        # Note : Si on rajoute une option, ne pas oublier d'ajouter la variable de contrôle à self._listData.append([variable, "texte explicatif", valeurParDefaut])
        # Note : Si l'option que l'on souhaite ajouter nécessite un redémarrage pour s'appliquer, utiliser la méthode "self.__addDataNeedRestart(liste)", avec la même liste que pour self._listData

        super().__init__(master, nom = "Profil", iid_parent ="-General", **kwargs)

        ## Widgets
        self.__frameLine1            = Frame(self._mFrame)
        self.__frameLine2            = Frame(self._mFrame)
        self.__frameLine3            = Frame(self._mFrame)
        # Ligne 1 : Nom du profil
        self.__lbProfil              = Label(self.__frameLine1, text="Profil :")
        self.__etProfil              = Entry(self.__frameLine1)
        # Ligne 2 : Label for folder location
        self.__lbPathCustomFile      = Label(self.__frameLine2, text = "Chemin d'enregistrement de vos fichiers de préférences")
        # Ligne 3 : Folder location
        self.__entryPathCustomFile   = Entry(self.__frameLine3, state="normal")
        self.__btnParcourir          = Button(self.__frameLine3, text = "...", command = self.__parcourir, width=3)


        # Affichage pour les widgets :
        self.__lbProfil           .pack(side = LEFT, padx = (2, 1))
        self.__etProfil           .pack(side = LEFT, padx = (1, 2), fill = X, expand = YES)

        self.__lbPathCustomFile   .pack(side = LEFT, padx = 2, fill = X)

        self.__entryPathCustomFile.pack(side = LEFT,  padx = (2, 1), fill = X, expand = YES)
        self.__btnParcourir       .pack(side = RIGHT, padx = (1, 2))

        # Et pour les lignes
        self.__frameLine1         .pack(side = TOP,  pady = (2, 1), fill = X)
        self.__frameLine2         .pack(side = TOP,  pady = (1, 1), fill = X)
        self.__frameLine3         .pack(side = TOP,  pady = (1, 2), fill = X)

        # Fonction de paramétrage
        profil = self.getProfilManager().getProfilActif() or self.getProfilManager().getListeProfilsUser()[0]

        # Update le nom :
        self.__etProfil.insert(0, profil)
        self.__etProfil.config(state = "readonly")

        # Update le path :
        self.__entryPathCustomFile.set(self.getProfilFolder(profil))

    ""
    ##############################
    # Méthodes liées à la page : #
    ##############################
    ""

    def __parcourir(self):
       """
       Fonction qui demande où stocker les fichier ET vérifie si le dossier est bien vide
       """
       path = askFolder(vide=True)

       # on set le nouveau path
       if path is not None:
           path += os.sep
           print("path :", path)
           self.__entryPathCustomFile.set(path)
           for file in os.listdir(self.getProfilFolder()):
               move(self.getProfilFolder()+os.sep+file, path)

           self.getProfilManager().saveNewPath(path, self.__etProfil.get())
           # On dit qu'un redémarrage est maintenant nécessaire # TODO : vérifier le code
           self.getFenetrePreferences().setRestartMode()

    ""
    ###################################
    # Méthodes liées à la fermeture : #
    ###################################
    ""
    def appliqueEffet(self, application):
        # TODO s'assurer que les profils sont au bon endroit.
        pass
