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
       self.__frameChoixProfil = Frame(self._mFrame)
       self.__lbProfil = Label(self.__frameChoixProfil, text="Profil :")
       self.__cbProfil = Combobox(self.__frameChoixProfil, state="readonly")
       self.__cbProfil.bind("<<ComboboxSelected>>", lambda e :self.__varEntryPath.set(self.getProfilManager().getProfilFolder(self.__cbProfil.get())))
       self.__btnAjouter = Button(self.__frameChoixProfil, text="Ajouter", command=self.__ajouter)
       # Folder location
       self.__lbPathCustomFile = Label(self._mFrame, text = "Chemin d'enregistrement de vos fichiers de préférences")
       self.__varEntryPath = StringVar()
       self.__entryPathCustomFile = Entry(self._mFrame, state="normal", textvariable = self.__varEntryPath)
       self.__btnParcourir = Button(self._mFrame, text = "...", command = self.__parcourir, width=3)


       # Affichage
       self.__frameChoixProfil.grid(column = 0, row = 0, sticky = "wens")
       self.__lbProfil.grid(column = 0, row = 0, sticky = "w")
       self.__cbProfil.grid(column = 1, row = 0, sticky="we")
       self.__btnAjouter.grid(column=2, row=0, sticky="e")
       self.__lbPathCustomFile.grid(column = 0, row = 1, sticky = "w")
       self.__entryPathCustomFile.grid(column = 0, row = 2, sticky = "we")
       self.__btnParcourir.grid(column = 1, row = 2, sticky = "w")

       # Fonction de parametrage
       self.__chargeProfil(self.getProfilManager().getProfilActif())
       self.__cbProfil.set(self.getProfilManager().getProfilActif())

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

    def __ajouter(self):
        """
        Fonction pour crée un nouveau profil
        """
        if self.getProfilManager().createProfil(False):
            self.__chargeProfil(self.getProfilManager().getListeProfilsUser()[-1])

    def __chargeProfil(self, profil):
        """
        Fonction qui va chercher les infos via le ProfilManager
        """
        self.__varEntryPath.set(self.getProfilFolder(profil))
        self.__cbProfil.config(value=self.getProfilManager().getListeProfilsUser()[:])
        self.__cbProfil.set(profil)

    def appliqueEffet(self, application):
       move(self.getProfilFolder(), self.__varEntryPath.get())
       # Si on change de profil
       if self.__cbProfil.get() != self.getProfilManager().getProfilActif():
           self.getProfilManager().switchProfil(self.__cbProfil.get())


