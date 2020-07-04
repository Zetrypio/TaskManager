# *-* coding:utf-8 *-*
from json import *
import os
from shutil import rmtree

from preferences.dialog.askProfil import *

NOMFICHIER = "Ressources/prefs/profils.json"

class ProfilManager:
    def __init__(self, app):
        """
        Classe qui s'occupe de manier les profils et de transmettres ses infos à la pageProfil
        """

        self.__app = app

        self.__profilActif = None

        self.__donnee = None

        self.__loadUserProfil()

    def getProfilActif(self):
        """
        @return self.__profilActif
        """
        return self.__profilActif

    def setProfilActif(self, profil):
        """
        Permet aussi de changer le nom de la fenetre
        @param profil : <str> nom du profil (doit être dans la liste)
        """
        if profil in self.getAllNomProfil():
            self.__profilActif = profil
            self.__app.winfo_toplevel().title(self.__app.winfo_toplevel().title().split(" - ")[0] + " - " + profil)


    def getListeProfilsUser(self):
        """
        @return self.__listeProfilsUser
        """
        return self.__donnee["user"][os.getlogin()]

    def getProfilFolder(self, profil = None):
        """
        @param profil : <str> contient le nom du profil
        @return path  : <str> contient le lien du dossier
        """
        if profil is None:
            profil = self.getProfilActif()
        return self.__donnee["profil"][profil]

    def getAllNomProfil(self):
        return self.__donnee["profil"]

    def getAllFolder(self):
        l = []
        for profil in self.__donnee["profil"]:
            l.append(self.__donnee["profil"][profil])
        return l

    def switchProfil(self, nouvProfil):
        """
        Permet de changer de profil
        @param nouvProfil : <str> indiquant le nouveau nom, permettant d'aller chercher le path
        """
        self.setProfilActif(nouvProfil)

        ## Changement de l'ordre des profils
        # Variable pour que la ligne d'après soit plus lisible
        listProfil = self.__donnee["user"][os.getlogin()]
        listProfil.insert(0,listProfil.pop(listProfil.index(nouvProfil)))
        self.__donnee["user"][os.getlogin()] = listProfil
        self.__write()

        self.__loadProfil()

    def createProfil(self, obligatoire):
        """
        Permet de créer un profil
        @param obligatoire : <bool> True  = création d'un profil, pour un user si il en a 0
                                    False = création d'un profil, facultatif
        """
        nom, folderProfil = askProfil(obligatoire, self.__app, self.getAllNomProfil())
        if nom is None:
            return False
        self.__donnee["user"][os.getlogin()].append(nom)
        self.__donnee["profil"][nom] = folderProfil

        self.__write()
        return True

    def deleteProfil(self, profil):
        """
        Fonction qui supprime un profil du fichier json
        @param profil : <str> contient le nom du profil
        """

        # On supprime le profil de l'utilisateur
        del self.getListeProfilsUser()[self.getListeProfilsUser().index(profil)]

        # On cherche s'il existe pour d'autres utilisateurs
        autreUser = False
        for listProfil in self.__donnee["user"].values():
            if profil in listProfil:
                autreUser = True
        # Si personne d'autre utilise le profil
        if not autreUser:
            path = self.getAllNomProfil()[profil]
            # On supprime ce qu'il y a dedans
            rmtree(path)
            # On supprime le path
            del self.getAllNomProfil()[profil]

        # On finit par écrire
        self.__write()

    def saveNewPath(self, path, profil):
        """
        Fonction qui va juste changer le path du profil courrant
        @param path   : <str> contient le chemin du folder
        @param profil : <str> contient le nom du profil
        """
        self.__read()
        self.__donnee["profil"][profil] = path
        self.__write()

    def __loadUserProfil(self):
        """
        Permet de charger les profils de l'utilisateur
        """
        ## Lecture
        # On test si le fichier existe, sinon on le crée
        if not os.path.exists(NOMFICHIER):
            with open(NOMFICHIER, "w", encoding="utf-8") as f:
                f.write(dumps({"user":{}, "profil":{}}, indent=4))

        self.__read()

        # Si l'utilisateur n'est pas présent, on le crée + on créer un profil
        if os.getlogin() not in self.__donnee["user"]:
            self.__donnee["user"][os.getlogin()] = []
            if not self.createProfil(True):
                return

        self.setProfilActif(self.getListeProfilsUser()[0])

        self.__loadProfil()

    def __loadProfil(self):
        """
        Permet de charger les préférences du profil actif
        """
        print(self.__profilActif, self.getProfilFolder())


    def __read(self):
        # On lit le fichier
        with open(NOMFICHIER,"r", encoding="utf-8") as f:
            self.__donnee = load(f)

    def __write(self):
        # On écrit dessus
        with open(NOMFICHIER, "w", encoding="utf-8") as f:
            f.write(dumps(self.__donnee, indent=4))

