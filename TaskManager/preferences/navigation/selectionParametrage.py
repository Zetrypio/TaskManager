# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk     import *
from tkinter import Label, Frame

class SelectionParametrage(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Note : self.master est une références vers NavigationZone


        ## ZE treeview
        self.tv = Treeview(self)

        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tv.yview)



    def onclick(self, e):
        # On récupère la cage qu'on a cliqué
        iidPageSelectionne = self.tv.focus()
        self.getFenetrePreferences().setPageActive(iidPageSelectionne)

    def getNavigationZone(self):
        return self.master

    def getFenetrePreferences(self):
        return self.getNavigationZone().getFenetrePreferences()

    def getZoneParametrage(self):
        return self.zoneParam

    def updateTreeview(self):
        # On efface tout
        self.tv.destroy()
        self.scrollbar.destroy()

        # On recrée tout
        self.tv = Treeview(self)
        self.tv.bind("<ButtonRelease-1>", self.onclick)
        self.tv.pack(side = LEFT, fill = BOTH, expand = YES)

        # Avec la scrollbar
        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tv.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tv.configure(yscrollcommand = self.scrollbar.set)

        # Les lignes
        for page in self.getFenetrePreferences().getListePage():
            page.ajouteToiTreeview(self.tv)

    def getApplication(self):
        return self.master.getApplication()
