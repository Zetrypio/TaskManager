# *-* coding:utf-8 *-*
from json import *
import os

NOMFICHIER = "clavier"

class BindingManager:
    def __init__(self, app):
        """
        Classe qui s'occupe d'enregistrer les bindings au format json
        """
        self.__app = app

        self.__donneePref = None
        self.__donneeUtil = None
        self.__donnee = None # Addition des 2 précédents

        self.__read()

    def __read(self, lireCfg = True, lireDef = True):
        """
        Permet de lire les fichiers
        @param lireCfg = <bool> lit ou pas le json de l'utilisateur
        @param lireDef = <bool> lit ou pas le json par défaut
        """
        if lireCfg:
            if os.path.exists(self.getProfilFolder() + NOMFICHIER + ".json"):
                with open(self.getProfilFolder() + NOMFICHIER + ".json", "r", encoding="utf-8") as f:
                    self.__donneeUtil = load(f)
            else:
                self.__donneeUtil = {}

        if lireDef:
            if os.path.exists("Ressources/prefs/" + NOMFICHIER + ".json"):
                with open("Ressources/prefs/" + NOMFICHIER + ".json", "r", encoding="utf-8") as f:
                    self.__donneePref = load(f)
            else:
                with open("Ressources/prefs/" + NOMFICHIER + ".json", "w", encoding="utf-8") as f: # TODO, faire un dico des bindings
                    f.write(dumps({"user":{}, "profil":{}}, indent=4))
                with open("Ressources/prefs/" + NOMFICHIER + ".json", "r", encoding="utf-8") as f:
                    self.__donneePref = load(f)


        for key in self.__donneePref:
            if not key in self.__donneeUtil:
                self.__donneeUtil[key] = self.__donneePref[key]

        self.__donnee = self.__donneeUtil
        print("Donnee :",self.__donnee)

    def getProfilFolder(self):
        return self.getApplication().getProfilManager().getProfilFolder(None)

    def getApplication(self):
        return self.__app

    def getBinding(self):
        return self.__donnee
