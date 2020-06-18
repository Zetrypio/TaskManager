# *-* coding:utf-8 *-*
from json import *
import os

from preferences.dialog.askProfil import *

NOMFICHIER = "Ressources/prefs/profils.json"

class ProfilManager:
    def __init__(self, app):
        """
        Classe qui s'occupe de manier les profils et de transmettres ses infos à la pageProfil
        """

        self.__app = app

        self.__profilActif          = None
        self.__listeProfilsUser     = None

        self.__loadProfil()

    def getProfilActif(self):
        """
        @return self.__profilActif
        """
        return self.__profilActif

    def getListeProfilsUser(self):
        """
        @return self.__listeProfilsUser
        """
        return self.__listeProfilsUser

    def getProfilFolder(self):
        """
        @return path : <str> contient le lien du dossier
        """
        with open(NOMFICHIER,"r") as f:
            data = load(f)
        return data["profil"][self.__profilActif]

    def switchProfil(self, nouvProfil):
        """
        Permet de changer de profil
        @param nouvProfil : <str> indiquant le nouveau nom, permettant d'aller chercher le path
        """
        """
        self.__profilActif = nouvProfil
        self.__loadProfil()
        """
        pass

    def createProfil(self):
        """
        Permet de créer un profil
        """
        pass

    def __loadUserProfil(self):
        """
        Permet de charger les profils de l'utilisateur
        """
        pass

    def __loadProfil(self):
        """
        Permet de charger les données du profil
        """
        ## Lecture
        # On test si le fichier existe, sinon on le crée
        if not os.path.exists(NOMFICHIER):
            with open(NOMFICHIER, "w") as f:
                f.write(dumps({"user":{}, "profil":{}}, indent=4))

        # On lit le fichier
        with open(NOMFICHIER,"r") as f:
            data = load(f)

        # On regarde si les valeurs existes
        try:
            self.__listeProfilsUser = data["user"][os.getlogin()]
            self.__profilActif = self.__listeProfilsUser[0]
        except:
            print("a")
            self.__profilActif, folderProfil = askProfil(True, self.__app)
            self.__listeProfilsUser = [self.__profilActif]
            data = {"user" : {os.getlogin() : [self.__profilActif]}, "profil":{self.__profilActif : folderProfil}}
            with open(NOMFICHIER, "w") as f:
                f.write(dumps(data, indent=4))

