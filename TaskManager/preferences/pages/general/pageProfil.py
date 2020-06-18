# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from shutil import move
import os

from ..AbstractPage import *



class PageProfil(AbstractPage):
    def __init__(self, master, **kwargs):
        # Note : self.master renvoie a ParametrageZone
       super().__init__(master, nom = "Profil", iid_parent ="-General", **kwargs)

       ## Widgets
       self.__lbProfil = Label(self._mFrame, text="Profil :")
       self.__cbProfil = Combobox(self._mFrame, state="readonly")
       # Folder location
       self.__lbPathCustomFile = Label(self._mFrame, text = "Chemin d'enregistrement de vos fichiers de préférences")
       self.__varEntryPath = StringVar()
       self.__entryPathCustomFile = Entry(self._mFrame, state="normal", textvariable = self.__varEntryPath)
       self.__btnParcourir = Button(self._mFrame, text = "...", command = self.__parcourir, width=3)


       # Affichage
       self.__lbProfil.grid(column = 0, row = 0, sticky = "w")
       self.__cbProfil.grid(column = 1, row = 0, sticky="we")
       self.__lbPathCustomFile.grid(column = 0, row = 1, sticky = "w")
       self.__entryPathCustomFile.grid(column = 0, row = 2, sticky = "we")
       self.__btnParcourir.grid(column = 1, row = 2, sticky = "w")

       # Fonction de parametrage
       self.__chargeProfil()

    def __parcourir(self):
       """
       fonction qui demande où stocker les fichier ET vérifie si le dossier est bien vide
       """
       path = askFolder(vide=True)
       # On bouge les fichiers en place
       #move(self.__varEntryPath.get(), path) Pas en place à cause d'un soucis de première location d'enregistrement

       # on set le nouveau path
       if path is not None:
           self.__varEntryPath.set(path)

    def __chargeProfil(self):
        """
        Fonction qui va chercher la position de sauvegarde des fichiers
        Pour : parametrer le combobox des profils
               remplir le champs du dossier d'enregistrement
        """
        """## Lecture
        # On test si le fichier existe, sinon on le crée
        if not os.path.exists(NOMFICHIER):
            with open(NOMFICHIER, "w") as f:
                f.write(dumps({"user":{}, "profil":{}}, indent=4))

        # On lit le fichier
        with open(NOMFICHIER,"r") as f:
            data = load(f)

        # On regarde si les valeurs existes
        try:
            listNomProfil = data["user"][os.getlogin()]
            nomProfil = listNomProfil[0]
            folderProfil  = data["profil"][nomProfil]
        except:
            nomProfil, folderProfil = askProfil(True, self.getApplication())
            data = {"user" : {os.getlogin() : nomProfil}, "profil":{nomProfil : folderProfil}}
            with open(NOMFICHIER, "w") as f:
                f.write(dumps(data, indent=4))"""

        self.__varEntryPath.set(self.getProfilManager().getProfilFolder())

        self.__cbProfil.config(value=self.getProfilManager().getListeProfilsUser())
        self.__cbProfil.set(self.getProfilManager().getProfilActif()[0])

    def getProfilManager(self):
        return self.getApplication().getProfilManager()

    def appliqueEffet(self, application):
       pass



