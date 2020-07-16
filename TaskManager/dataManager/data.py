# *-* coding:utf-8 *-*
from configparser import *
import os

class Data(ConfigParser):
    def __init__(self):
        super().__init__(self)
        # Création des attributs
        self.__currentThemeName = "Classique"
        self.__profilFolder = None

    "" # Marque pour le repli
    ################
    # Utilitaire : #
    ################
    ""
    def read(self, fichier, add = False):
        """
        On efface ce qu'on avait en mémoire
        et on relie tout
        """
        if not add:
            self.clear()
        super().read(fichier, encoding="utf-8")

    def readFile(self, nom, lireDef = True, lireCfg = True):
        """
        Fonction qui va lire les fichiers de préférences avec Data
        @param nom : <str> nom du fichier à lire (sans l'extension)
        """
        self.clear()
        if lireDef and lireCfg:
            self.read("Ressources/prefs/"+nom+".def")
            if os.path.exists(self.getProfilFolder() + nom + ".cfg"):
                self.read(self.getProfilFolder() + nom + ".cfg", add=True) # Prise de conscience de ce qu'il y a dedans

        # On ne met pas le add sinon
        elif not lireDef and lireCfg:
            if os.path.exists(self.getProfilFolder() + nom + ".cfg"):
                self.read(self.getProfilFolder() + nom + ".cfg") # Prise de conscience de ce qu'il y a dedans
        elif lireDef and not lireCfg:
            self.read("Ressources/prefs/"+nom+".def")

    def sauv(self, fichier):
        """
        Ecrit dans le fichier puis
        @param fichier : <str> contient le path + nom + extension du fichier dans lequel Data doit écrire
        # Note : une lecture de ce fichier est conseillé avant afin de ne pas supprimer tout le contenu inutilement
        """
        with open(fichier, "w", encoding="utf-8") as tfile:
            self.write(tfile)

    ""
    #############
    # Testeur : #
    #############
    ""
    def testBool(self, value):
       """ Test pour savoir si value est un Booléen """
       if not isinstance(value, bool):
           raise TypeError("Exptected a boolean")

    def testString(self, value):
       """ Test pour savoir si value est un String """
       if not isinstance(value, str):
           raise TypeError("Exptected a string")

    ""
    ###########
    # Getters #
    ###########
    ""
    def getProfilFolder(self):
        return self.__profilFolder

    ""
    ###########
    # Setters #
    ###########
    ""
    def setProfilFolder(self, value):
        """
        Setter du path du profil en cours
        @param value : <str> contient le path
        """
        self.testString(value)
        self.__profilFolder = value
        return
