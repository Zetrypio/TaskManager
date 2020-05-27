# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

class AbstractPage(Frame):
    def __init__(self, master, nom, parent = "", **kwargs):
        super().__init__(master, **kwargs)
        self.nom = nom
        self.parent = parent
        self.iid = self.getParent()+"-"+self.getNom()

    def getNom(self):
        return self.nom

    def getParent(self):
        """ Retourne la page parente du treeview """
        return self.parent

    def getIid(self):
        return self.iid

    def ajouteToiTreeview(self, treeview):
        """
        Fonction qui permet l'affichage de la page dans le treeview
        @param treeview : <tkinter.treeview> le treeview sur lequelle on doit s'afficher
        """
        treeview.insert(self.getParent(), END, text=self.getNom(), iid=self.getIid())
