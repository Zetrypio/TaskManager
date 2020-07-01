# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..AbstractPage import *
from preferences.dialog.askResetBind import *

NOMFICHIER = "clavier"

class PageClavier(AbstractPage):
    def __init__(self, master, **kwargs):
        """
        Classe qui s'occupe d'afficher les bindings
        """
        # Note : self.master renvoie a ParametrageZone
        super().__init__(master,nom = "Clavier", iid_parent ="-General", **kwargs)

        self.__lineSelectedTreeview = None
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


        ## Frame du bas
        self.__frameBas = Frame(self._mFrame)
        self.__btnSave = Button(self.__frameBas, text = "Sauvegarder", command = self.__save)
        self.__lbListConflit = Label(self.__frameBas, text = "Liste des conflits :")
        self.__varListConflit = StringVar()
        self.__listConflit = Listbox(self.__frameBas, listvariable = self.__varListConflit)
        self.__lbChampBind = Label(self.__frameBas, text="Combinaison de touches :")
        self.__btnReset = Button(self.__frameBas, text = "Reset", command = self.__reset)
        # Le champ d'entrée
        self.__varEntry = StringVar()
        okCommand = self._mFrame.register(self.__focusOut)
        self.__champBind = Entry(self.__frameBas, textvariable = self.__varEntry, validatecommand=okCommand, validate="focusout", state  ="#A83FC5")

        # Affichage
        self.__frameBas.pack(side = BOTTOM, fill = BOTH)
        self.__lbListConflit.pack(side = TOP, anchor = "e", padx=28)
        self.__listConflit.pack(side = RIGHT, fill = BOTH,expand = YES, padx=3)
        self.__lbChampBind.pack(side = TOP, fill = Y, anchor = "w")
        self.__champBind.pack(side = TOP, fill = X)
        self.__btnSave.pack(side = RIGHT)
        self.__btnReset.pack(side = RIGHT)


        self.__treeB.pack(expand = YES, fill = BOTH, side = LEFT)
        self.__scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)

        # Final
        self.fillTreeView()
        self.__stateFrameBas("disabled")

    def fillTreeView(self):
        """
        Fonction qui rajoute toutes lignes de bind du treeview
        """
        #Parcours des sections (qui sont des ensembles)

        for section in self.getBindings():
            self.__treeB.insert("", END,iid=section, text= section.capitalize(), open=True, tag="header")
            for binding in self.getBindings()[section]:
                bd = self.getBindings()[section][binding]
                self.__listeItemTreeview.append(self.__treeB.insert(section, END,iid=section+binding, text=binding.capitalize(), value=(bd["description"], "; ".join(bd["bindings"]))))


        self.__treeB.tag_configure("header", font="arial 10 bold") # à voir si on garde une stylisation comme ça

    def __valueLineTV(self, item):
        """
        Fonction qui va chercher des info sur la ligne du treeview qu'on lui donne
        @param item      : <item (ligne Treeview)>
        @return section  : <str>  nom de la section du bind
        @return nom      : <str>  nom du binding virtuel
        @return binding  : <list> chaine de caractère du bind
        """
        nom = self.__treeB.item(item, "text").lower()
        section = item[0:len(item)-len(nom)] # retourne un str avec la section
        binding = self.__treeB.item(item, "value")[1].split('; ') # Les Raccourcis
        return section, nom, binding

    def __save(self):
        """
        Fonction qui sauvegarde les préférences.
        """
        # On commence par faire un dico
        dict = self.getBindings()
        # Ensuite on le change avec les nouvelles options
        print(dict)
        for item in self.__listeItemTreeview:
            s, n, b = self.__valueLineTV(item)
            print("section :", s, "\nnom :", n, "\nbinding :", b)
            dict[s][n]["bindings"] = b

        self.getBindingManager().save(dict)

    def __reset(self):
        """
        Fonction qui réattribut un ancien binding choisi par askResetBind
        """
        binding = askResetBind() # renvoie "custom", "defaut", "vide" ou None
        if binding is None:
            return
        else: # Sinon on va chercher quelle ligne on doit changer
            cur = self.__treeB.focus()
            s, n, b = self.__valueLineTV(cur)
        # Quel fichier on cherche ?
        if binding == "custom":
            path = self.getProfilFolder()
        elif binding == "defaut":
            path = "Ressources/prefs/"
        elif binding == "vide":
            self.__varEntry.set("")
            self.__treeB.item(cur, value=[self.__treeB.item(cur, "value")[0], self.__varEntry.get()])
            return
        # On applique le changement
        self.__varEntry.set(self.getBindingManager().getBind(path, s, n))
        self.__treeB.item(cur, value=[self.__treeB.item(cur, "value")[0], self.__varEntry.get()])


    def __selected(self, e):
        """
        Fonction qui réagit lorsqu'une ligne du treeview est sélectionné
        Ça gère si on doit faire qqch avec le frame du bas
        + Si c'est une ligne de binding on l'Entry s'auto set avec le binding
        """
        elem = self.__lineSelectedTreeview = self.__treeB.focus()
        if elem in self.__listeItemTreeview:
            self.__stateFrameBas("normal")
            self.__checkConflit(elem)
            self.__varEntry.set(self.__treeB.item(elem, 'value')[1])
        else:
            self.__stateFrameBas("disabled")

    def __stateFrameBas(self, mode):
        """
        Fonction qui s'occupe de able ou disable les option du frame du bas
        @param mode : <str> "normal" ou "disabled", else error
        """
        self.__btnReset.config(state = mode)
        self.__champBind.config(state = mode)
        self.__listConflit.config(state = mode)

    def __focusOut(self):
        """
        Fonction qui va réécrir les lignes du treeview, dès que le focus du Entry est perdu
        """
        if self.__lineSelectedTreeview in self.__listeItemTreeview:
            if self.__varEntry.get() != "":
                # on set la value de l'item selectionné en [sa description, le texte de l'entry]
                self.__treeB.item(self.__lineSelectedTreeview, value=[self.__treeB.item(self.__lineSelectedTreeview, "value")[0], self.__varEntry.get()])
                # on check les conflits
                self.__checkConflit(self.__lineSelectedTreeview)
        return True

    def __checkConflit(self, item):
        """
        Fonction qui cherche si le binding actuelle est en conflit avec d'autres bindings
        @param item : <item (ligne de Treeview)> celui qui vient d'être changé
        """
        # On retire le tag "conflit" à tout le monde
        for line in self.__listeItemTreeview:
            if self.__treeB.tag_has("conflict", line):
                nouvTags = list(self.__treeB.item(line, "tags")).remove("conflict")
                if nouvTags is None:
                    nouvTags = []
                self.__treeB.item(line, tags=nouvTags)
        # On fait une liste pour aller dans le Listbox
        l = []
        sectionItem, nomItem, bindingItem = self.__valueLineTV(item)
        # On parcours les bindings pour trouver correspondances
        for line in self.__listeItemTreeview:
            bindingConflictuel = set(self.__treeB.item(line, "value")[1].split("; ")).intersection(bindingItem)
            if bindingConflictuel != set() and bindingConflictuel != set(""):
                    if line != item:
                        sectionConflit, nomConflit, bindingConflit = self.__valueLineTV(line)
                        # On ajoute le nom du Binding virtuel à la liste
                        l.append(sectionConflit + " - " + nomConflit)
                        # On ajoute le tag "conflit à la liste
                        t = list(self.__treeB.item(line, "tags"))
                        t.append("conflict")
                        self.__treeB.item(line, tag=t)
                        self.__treeB.tag_configure("conflict", foreground="red")

        # S'il y a qqch dans la liste on rajoute celui qu'on fait pour une meilleur lisibilité
        if l:
            t = list(self.__treeB.item(item, "tags"))
            t.append("conflict")
            self.__treeB.item(item, tag=t)
            l.append(sectionItem + " - " + nomItem)
        # On connecte notre liste à la listbox
        self.__varListConflit.set(l)

    def getBindings(self):
        """
        @return un dictionnaire des bindings
        """
        return self.getBindingManager().getBindings()

    def getBindingManager(self):
        return self.getApplication().getBindingManager()

    def appliqueEffet(self, application):
        self.__save()
