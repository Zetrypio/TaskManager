# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label
import os

class AbstractPage(Frame):
    def __init__(self, master, nom = "Inconnu", iid_parent = "", **kwargs):
        # Note : self.master renvoie vers ParametrageZone
        # Note : Si on rajoute une option ne pas oublier d'ajouter la variable de controle à self._listData.append([variable, "texte explicatif"])

        super().__init__(master, **kwargs)
        self.nom = nom
        self.iidParent = iid_parent
        self.iid = self.getParent()+"-"+self.getNom()

        self._listData = [] # C'est une liste qui contient toutes les variables de controles à enregistrer + les key pour le dico [variable, text]

        self._mFrame = Frame(self)
        self.__lbTitre = Label(self, text=self.nom)
        self.__sepTitre = Separator(self, orient=HORIZONTAL)


        self._mFrame.pack(side = BOTTOM, expand = YES, fill = BOTH)
        self.__sepTitre.pack(side = BOTTOM, fill = X)
        self.__lbTitre.pack(side = LEFT, fill = X)

    def getNom(self):
        return self.nom

    def getParent(self):
        """ Retourne la page parente du treeview """
        return self.iidParent

    def getIid(self):
        return self.iid

    def getProfilManager(self):
        return self.getApplication().getProfilManager()

    def getProfilFolder(self, profil = None):
        return self.getProfilManager().getProfilFolder(profil)

    def readFile(self, nom, lireDef = True, lireCfg = True):
        """
        Fonction qui va lire les fichiers de préférences
        @param nom : <str> nom du fichier à lire (sans l'extension)
        """
        self.getData().clear()
        if lireDef and lireCfg:
            self.getData().read("Ressources/prefs/"+nom+".def")
            if os.path.exists(self.getProfilFolder() + nom + ".cfg"):
                self.getData().read(self.getProfilFolder() + nom + ".cfg", add=True) # Prise de conscience de ce qu'il y a dedans

        # On ne met pas le add sinon
        elif not lireDef and lireCfg:
            if os.path.exists(self.getProfilFolder() + nom + ".cfg"):
                self.getData().read(self.getProfilFolder() + nom + ".cfg") # Prise de conscience de ce qu'il y a dedans
        elif lireDef and not lireCfg:
            self.getData().read("Ressources/prefs/"+nom+".def")

    def _loadDataFile(self):
        """
        Fonction qui va chercher la variable demandé
        """
        pass

    def _makeDictAndSave(self):
        """
        Fonction qui fabrique un dictionnaire à partir des values de _listData
        """
        # nomFichier : <str> nom de la superPage pour en faire le nom du fichier
        nomFichier = self.getNom() if len(self.getParent().split("-")) <= 1 else self.getParent().split("-")[1]
        # section    : <str> nom de la page courante
        section = self.getNom()
        pathFile = self.getProfilFolder() + nomFichier + ".cfg"
        # On cherche s'il y a des info dedans avant de tout overrider
        if os.path.exists(pathFile):
            self.getData().read(pathFile)
        else:
            self.getData().clear()

        # On créer le dico
        dict = {}
        # On compile tout
        for donnee in self._listData:
            dict[donnee[1]] = donnee[0].get()
        # Et on enregistre
        self.getData()[section] = dict
        self.getData().sauv(pathFile)

    def appliqueEffet(self, application):
        raise NotImplementedError

    def ajouteToiTreeview(self, treeview):
        """
        Fonction qui permet l'affichage de la page dans le treeview
        @param treeview : <tkinter.treeview> le treeview sur lequelle on doit s'afficher
        """
        treeview.insert(self.getParent(), END, text=self.getNom(), iid=self.getIid())

    def getParametrageZone(self):
        return self.master

    def getApplication(self):
        return self.master.getApplication()

    def getData(self):
        return self.getApplication().getData()
