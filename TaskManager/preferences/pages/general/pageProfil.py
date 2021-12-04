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
       self.__frameChoixProfil = Frame(self._mFrame)
       self.__lbProfil = Label(self.__frameChoixProfil, text="Profil :")
       self.__cbProfil = Combobox(self.__frameChoixProfil, state="readonly")
       self.__cbProfil.bind("<<ComboboxSelected>>", lambda e :self.__varEntryPath.set(self.getProfilManager().getProfilFolder(self.__cbProfil.get())))
       self.__btnAjouter   = Button(self.__frameChoixProfil, text="Ajouter",   command=self.__ajouter)
       self.__btnSupprimer = Button(self.__frameChoixProfil, text="Supprimer", command=self.__supprimer)
       # Folder location
       self.__lbPathCustomFile = Label(self._mFrame, text = "Chemin d'enregistrement de vos fichiers de préférences")
       self.__varEntryPath = StringVar()
       self.__entryPathCustomFile = Entry(self._mFrame, state="normal", textvariable = self.__varEntryPath)
       self.__btnParcourir = Button(self._mFrame, text = "...", command = self.__parcourir, width=3)


       # Affichage
       self.__frameChoixProfil   .grid(column = 0, row = 0, sticky = "wens")
       self.__lbProfil           .grid(column = 0, row = 0, sticky = "w")
       self.__cbProfil           .grid(column = 1, row = 0, sticky = "we")
       self.__btnAjouter         .grid(column = 2, row = 0, sticky = "e")
       self.__btnSupprimer       .grid(column = 3, row = 0, sticky = "e")
       self.__lbPathCustomFile   .grid(column = 0, row = 1, sticky = "w")
       self.__entryPathCustomFile.grid(column = 0, row = 2, sticky = "we")
       self.__btnParcourir       .grid(column = 1, row = 2, sticky = "w")

       # Fonction de paramétrage
       self.__chargeProfil(self.getProfilManager().getProfilActif())

    ""
    #############################################
    # Méthodes liées à la gestion des profils : #
    #############################################
    ""
    def __ajouter(self):
        """
        Fonction pour crée un nouveau profil
        """
        if self.getProfilManager().createProfil(False):
            self.__chargeProfil(self.getProfilManager().getListeProfilsUser()[-1])

    def __supprimer(self):
        """
        Fonction qui supprimer un profil
        """
        # S'il n'y a qu'un seul profil
        if len(self.__cbProfil.cget("value")) == 1:
            showerror(title = "Suppression impossible", message = "Vous ne pouvez pas supprimer votre seul profil")
            return

        # On pose la question
        if not askyesnowarning(title = "Supprimer un thème", message = "Voulez-vous vraiment supprimer \"%s\" de vos profils ?\nSi vous êtes le seul utilisateur, cela supprimera le dossier ainsi que tout ce qui s'y trouve"%self.__cbProfil.get()):
            return

        self.getProfilManager().deleteProfil(self.__cbProfil.get())
        # On remet un nouveau profil
        self.__chargeProfil(None)

    ""
    ##############################
    # Méthodes liées à la page : #
    ##############################
    ""
    def __chargeProfil(self, profil):
        """
        Fonction qui va chercher les infos via le ProfilManager
        @param profil : <str> nom du profil a charger
                        if None : profil = 1er profil de la liste
        """
        self.__cbProfil.config(value=self.getProfilManager().getListeProfilsUser()[:])

        # On prend le premier profil si c'est None en paramètre
        profil = self.__cbProfil.cget("value")[0] if profil is None else profil

        self.__varEntryPath.set(self.getProfilFolder(profil))
        self.__cbProfil.set(profil)

    def __parcourir(self):
       """
       Fonction qui demande où stocker les fichier ET vérifie si le dossier est bien vide
       """
       path = askFolder(vide=True)

       # on set le nouveau path
       if path is not None:
           path += os.sep
           print("path :", path)
           self.__varEntryPath.set(path)
           for file in os.listdir(self.getProfilFolder()):
               move(self.getProfilFolder()+os.sep+file, path)

           self.getProfilManager().saveNewPath(path, self.__cbProfil.get())
           # On dit qu'un redemarrage est maintenant nécéssaire
           self.getFenetrePreferences().setRestartMode()

    ""
    ###################################
    # Méthodes liées à la fermeture : #
    ###################################
    ""
    def appliqueEffet(self, application):
        # Si on change de profil
        if self.__cbProfil.get() != self.getProfilManager().getProfilActif():
           self.getProfilManager().switchProfil(self.__cbProfil.get())
