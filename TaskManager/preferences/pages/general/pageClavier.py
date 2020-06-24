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
        self.__listeSection = []
        # La config :
        self.__treeB.heading("#0",text="Nom",anchor="w")
        self.__treeB.heading("2", text="Description",anchor="w")
        self.__treeB.heading("3", text="Raccourci",anchor="w")

        # Scrollbar
        self.__scrollbar = Scrollbar(self._mFrame, orient = VERTICAL, command = self.__treeB.yview)
        self.__treeB.configure(yscrollcommand = self.__scrollbar.set)


        # Frame du bas
        self.__frameBas = Frame(self._mFrame)
        self.__btnSave = Button(self.__frameBas, text = "Sauverager", command = self.__save)
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
        """
        self.__read(NOMFICHIER)
        for index, section in enumerate(self.getData().sections()):
            self.__treeB.insert("", END,iid=section, text= section.capitalize(), open=True, tag="header")
            self.__listeSection.append([])
            k = self.getData()[section]
            print(k)
            #for key in self.getData()[section]:
            #    self.__listeSection[index].append(self.__treeB.insert(section, END,iid = section + k, text = k, value=("Permet de quitter l'application", "Esc")))
        """
        self.a = self.__treeB.insert("", END, iid="general", text="Général", open=True, tag="header")
        self.b = self.__treeB.insert("general", END, "moi", text = "Quitter", value=("Permet de quitter l'application", "Esc"))
        self.c = self.__treeB.insert("general", END, "moib", text = "Ouvrir", value=("Permet d'ouvrir un fichier", "Ctrl + O"))
        self.__treeB.tag_configure("header", font="arial 10 bold") # à voir si on garde une stylisation comme ça

    def __save(self):
        """
        Fonction qui sauvegarde les préférences.
        """
        self.__treeB.selection_set(self.a)
        print("test :", "a")

    def __reset(self):
        """
        Fonction qui réattribut l'ancien binding
        """
        pass

    def __selected(self, e):
        elem = self.__treeB.focus()
        if elem in self.__listeSection:
            print("oui")
            self.stateFrameBas("normal")
        else:
            self.stateFrameBas("disabled")

    def stateFrameBas(self, mode):
        """
        Fonction qui s'occupe de able ou disable les option du frame du bas
        @param mode : <str> "normal" ou "disabled", else error
        """
        self.__btnReset.config(state = mode)
        self.__btnSave.config(state = mode)
        self.__champBind.config(state = mode)
        self.__listConflit.config(state = mode)

    def appliqueEffet(self, application):pass
