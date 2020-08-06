# *-* coding:utf-8 *-*
from configparser import *
import os

class Data(ConfigParser):
    def __init__(self):
        super().__init__(self)
        # Création des attributs
        self.__currentThemeBg = None
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

    def testDataExist(self, nomFichier, nomSection, nomCle):
        """
        Méthode qui True si la valeur existe dans le fichier et la section indiqué
        @param nomFichier : <str> contient le nom du fichier dans lequel se trouve notre valeur
        @param nomSection : <str> contient le nom de la section dans laquelle se trouve notre valeur
        @param nomCle     : <str> contient le nom de la clé pour ainsi obtenir la valeur
        @return : True = la clé exsite, False = la clé, la section ou le fichier n'existe pas
        """
        self.readFile(nomFichier)
        return True if nomSection in self.sections() and nomCle in self[nomSection] else False

    def testString(self, value):
       """ Test pour savoir si value est un String """
       if not isinstance(value, str):
           raise TypeError("Exptected a string")

    ""
    ###########
    # Getters #
    ###########
    ""
    def getCurrentThemeBg(self):
        return self.__currentThemeBg

    def getOneValue(self, nomFichier, nomSection, nomCle):
        """
        Méthode qui renvoie une valeur précise
        @param nomFichier : <str> contient le nom du fichier dans lequel se trouve notre valeur
        @param nomSection : <str> contient le nom de la section dans laquelle se trouve notre valeur
        @param nomCle     : <str> contient le nom de la clé pour ainsi obtenir la valeur
        @return : la value
        """
        if not self.testDataExist(nomFichier, nomSection, nomCle):
            raise ValueError("%s n'existe pas dans %s du fichier %s.\n utiliser la méthode data.testDataExist() pour éviter l'erreur"%(nomCle, nomSection, nomFichier))
        return self[nomSection][nomCle]

    def getProfilFolder(self):
        return self.__profilFolder

    ""
    ###########
    # Setters #
    ###########
    ""
    def setCurrentThemeBg(self, value):
        """
        Setter de la couleur de background de la palette Tk
        @param value : <str> code couleur pour tk
        """
        self.testString(value)
        self.__currentThemeBg = value
        return

    def setProfilFolder(self, value):
        """
        Setter du path du profil en cours
        @param value : <str> contient le path
        """
        self.testString(value)
        self.__profilFolder = value
        return
