# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..AbstractPage import *

NOMFICHIER = "clavier"

class PageClavier(AbstractPage):
    def __init__(self, master, **kwargs):
        """
        Classe qui s'occupe d'afficher les bindings
        """
        # Note : self.master renvoie a ParametrageZone
        super().__init__(master,nom = "Clavier", iid_parent ="-General", **kwargs)

        ## Treeview
        self.__treeB = Treeview(self._mFrame, columns = ("2", "3"))
        self.__treeB.bind("<<TreeviewSelect>>", self.__selected)
        self.__listeItemTreeview = []
        # La config :
        self.__treeB.heading("#0",text="Nom",anchor="w")
        self.__treeB.heading("2", text="Description",anchor="w")
        self.__treeB.heading("3", text="Raccourci",anchor="w")

        # Scrollbar
        self.__scrollbar = Scrollbar(self._mFrame, orient = VERTICAL, command = self.__treeB.yview)
        self.__treeB.configure(yscrollcommand = self.__scrollbar.set)


        # Frame du bas
        self.__frameBas = Frame(self._mFrame)
        self.__btnSave = Button(self.__frameBas, text = "Sauvegarder", command = self.__save)
        self.__lbListConflit = Label(self.__frameBas, text = "Liste des conflits :")
        self.__listConflit = Listbox(self.__frameBas)
        self.__lbChampBind = Label(self.__frameBas, text="Combinaison de touches :")
        self.__champBind = Entry(self.__frameBas)
        self.__btnReset = Button(self.__frameBas, text = "Reset", command = self.__reset)

        # Affichage
        self.__frameBas.pack(side = BOTTOM, fill = BOTH)
        self.__lbListConflit.pack(side = TOP, anchor = "e", padx=28)
        self.__listConflit.pack(side = RIGHT, fill = Y, padx=3)
        self.__lbChampBind.pack(side = TOP, fill = Y, anchor = "w")
        self.__champBind.pack(side = TOP, fill = X)
        self.__btnSave.pack(side = RIGHT)
        self.__btnReset.pack(side = RIGHT)


        self.__treeB.pack(expand = YES, fill = BOTH, side = LEFT)
        self.__scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)

        # Final
        self.fillTreeView()
        self.stateFrameBas("disabled")

    def fillTreeView(self):
        """
        Fonction qui rajoute toutes lignes de bind du treeview
        """
        #Parcours des sections (qui sont des ensembles)

        for section in self.getBinding():
            self.__treeB.insert("", END,iid=section, text= section.capitalize(), open=True, tag="header")
            for binding in self.getBinding()[section]:
                bd = self.getBinding()[section][binding]
                self.__listeItemTreeview.append(self.__treeB.insert(section, END,iid=section+binding, text=binding.capitalize(), value=(bd["description"], bd["bindings"])))


        self.__treeB.tag_configure("header", font="arial 10 bold") # à voir si on garde une stylisation comme ça

    def __save(self):
        """
        Fonction qui sauvegarde les préférences.
        """
        # On commence par faire un dico
        dict = self.getBinding()
        # Ensuite on le change avec les nouvelles options
        print(dict)
        for item in self.__listeItemTreeview:
            nom = self.__treeB.item(item, "text").lower()
            section = item[0:len(item)-len(nom)] # retourne un str avec la section
            binding = self.__treeB.item(item, "value")[1] # Les Raccourcis
            print("section :",section, "\nnom :", nom, "\nbinding :", binding)
            dict[section][nom]["bindings"] = binding

        self.getApplication().getBindingManager().save(dict)

    def __reset(self):
        """
        Fonction qui réattribut l'ancien binding
        """
        pass

    def __selected(self, e):
        elem = self.__treeB.focus()
        if elem in self.__listeItemTreeview:
            self.stateFrameBas("normal")
        else:
            self.stateFrameBas("disabled")

    def stateFrameBas(self, mode):
        """
        Fonction qui s'occupe de able ou disable les option du frame du bas
        @param mode : <str> "normal" ou "disabled", else error
        """
        self.__btnReset.config(state = mode)
        self.__champBind.config(state = mode)
        self.__listConflit.config(state = mode)

    def getBinding(self):
        """
        @return un dictionnaire des bindings
        """
        return self.getApplication().getBindingManager().getBinding()

    def appliqueEffet(self, application):pass
