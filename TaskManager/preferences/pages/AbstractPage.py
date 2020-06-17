# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

class AbstractPage(Frame):
    def __init__(self, master, nom = "Inconnu", iid_parent = "", **kwargs):
        # Note : self.master renvoie vers ParametrageZone
        super().__init__(master, **kwargs)
        self.nom = nom
        self.iidParent = iid_parent
        self.iid = self.getParent()+"-"+self.getNom()

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