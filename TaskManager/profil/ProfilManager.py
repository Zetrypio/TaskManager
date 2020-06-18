# *-* coding:utf-8 *-*
from json import *

class ProfilManager:
    def __init__(self, parent):
        """
        Classe qui s'occupe de manier les profils et de transmettres ses infos à la pageProfil
        """
        # Note : self.master renvoie à l'Application

        self.__profilActif         = None
        self.__listeProfilsUser     = None
        self.__listeProfilsPossible = None

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

    def getListeProfilsPossible(self):
        """
        @return self.__listeProfilsPossible
        """
        return self.__listeProfilsPossible

    def switchProfil(self):
        """
        Permet de changer de profil
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

    def __loadProfilPossible(self):
        """
        Permet de charger les profils auquels l'utilisateur à accès via sa session
        """
        pass

    def __loadProfil(self):
        """
        Permet de charger les données du profil
        """
        pass

    def __loadPreferences(self):
        """
        Permet de charger les préférences du profil
        """
        pass
