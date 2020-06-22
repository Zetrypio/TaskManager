# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..AbstractPage import *
from profil.BindingManager import *

class PageClavier(AbstractPage):
    def __init__(self, master, **kwargs):
        """
        Classe qui s'occupe d'afficher les bindings
        """
        # Note : self.master renvoie a ParametrageZone
        super().__init__(master,nom = "Clavier", iid_parent ="-General", **kwargs)

        self.__bindingManager = BindingManager(self.getApplication())

        ## Treeview
        self.__treeB = Treeview(self._mFrame, columns = ("2", "3"))
        # La config :
        self.__treeB.heading("#0",text="Nom",anchor="w")
        self.__treeB.heading("2", text="Description",anchor="w")
        self.__treeB.heading("3", text="Raccourci",anchor="w")

        # Scrollbar
        self.__scrollbar = Scrollbar(self._mFrame, orient = VERTICAL, command = self.__treeB.yview)
        self.__treeB.configure(yscrollcommand = self.__scrollbar.set)


        # Affichage
        self.__treeB.pack(expand = YES, fill = BOTH, side = LEFT)
        self.__scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)

        # Final
        self.fillTreeView()

    def fillTreeView(self):
        """
        Fonction qui rajoute toutes lignes de bind du treeview
        """
        self.__bindingManager.bindingInsertToi(self.__treeB)
        self.__treeB.insert("", END, "general", text="Général", open=True, tag="header")
        self.__treeB.insert("general", END, "moi", text = "Quitter", value=("Permet de quitter l'application", "Esc"))
        self.__treeB.insert("general", END, "moib", text = "Ouvrir", value=("Permet d'ouvrir un fichier", "Ctrl + O"))
        self.__treeB.tag_configure("header", font="arial 10 bold") # à voir si on garde une stylisation comme ça

    def appliqueEffet(self, application):pass
