# *-* coding:utf-8 *-*
from configparser import *

class Data(ConfigParser):
    def __init__(self):
        # Création des attributs
        self.__affichageNombreHorloge = True
        self.__currentThemeName = "Classique"
        self.__adaptColorTask = False
        self.__allowTtkButton = True

    def testBool(self, value):
        """ Test pour savoir si value est un Booléen """
        if not isinstance(value, bool):
            raise TypeError("Exptected a boolean")

    def testSrting(self, value):
        """ Test pour savoir si value est un String """
        if not isinstance(value, str):
            raise TypeError("Exptected a string")

    def getAffichageNombreHorloge(self):
        """ getter de l'affichage lié aux nombre sur les bords de l'horloge """
        return self.__affichageNombreHorloge

    def setAffichageNombreHorloge(self, value):
        """
        Setter de l'affichage lié aux nombre sur les bords de l'horloge
        @param value : <Bool> True = nombre, False = pas de nombre
        """
        self.testBool(value)
        self.__affichageNombreHorloge = value

    def getCurrentThemeName(self):
        """ getter du nom du thème actuel """
        return self.__currentThemeName

    def setCurrentThemeName(self, value):
        """
        Setter du nom du thème en place
        + changement du thème TODO
        @param value : <String> contient le nom, "test thème" = thème en cours de création et non enregistrée
        """
        self.testSrting(value)
        self.__currentThemeName = value

    def getAdaptColorTask(self):
        return self.__adaptColorTask

    def setAdaptColorTask(self, value):
        """
        Setter du mode si oui ou non on adapte la couleur du texte d'une tache en fonction de la couleur de fond
        @param value : <Bool> True = on adapt, False = on laisse comme ça
        """
        self.testBool(value)
        self.__adaptColorTask = value

    def getAllowTtkButton(self):
        """
        getter de la variable qui veux ou non des boutons de ttk
        """
        return self.__allowTtkButton

    def setAllowTtkButton(self, value):
        """
        setter du mode des ttk buttons
        """
        self.testBool(value)
        self.__allowTtkButton = value

