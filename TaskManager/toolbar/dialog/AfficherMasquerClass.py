# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.Dialog import *

from schedulable.task.Task import Task
from schedulable.groupe.Groupe import Groupe

from schedulable.task.TaskEditor import *

class AfficherMasquer(TaskEditor):
    """
    Classe qui permet d'allouer ou non l'affichage des schedulables
    """
    def __init__(self, master, periodManager, **kw):
        """
        @param master        : <tkinter.frame> là oùon veut notre widget
        @param periodManager : <PeriodManager> celui d'application
        @return masquage : <bool> True si QQch est caché
        """
        # Note : master est une référence vers le dialog
        Frame.__init__(self, master, **kw)

        self.listeModify = [] # Liste de tache a changer [tache][visible ?]
        self.iterScheduModify = [] # Liste de tache affecté par un changement depuis le lancement du dialog
        self.listOpen = [] # Liste de lignes (item de Treeview) ouverte
        self.listTreeItem = [] # Liste d'item de Treeview

        # Attributs normaux :
        #self.mousepress = False
        self.MODE_TRI = "None"

        self.taches = []
        self.__periodManager = periodManager

        # Pour pouvoir filtrer l'affichage :
        self.FILTRE = {}

        # Zone des recherche :
        self.frameRecherche = Frame(self)
        self.frameRecherche.pack(side = TOP, fill = X, pady = 5)
        Label(self.frameRecherche, text = "Rechercher :").pack(side = LEFT)
        self.barreRecherche = Combobox(self.frameRecherche)
        self.barreRecherche.pack(side = LEFT, fill = X, expand = YES)

        # Liste des 10 dernières recherches:
        self._dernieresRecherches = deque(maxlen=10)

        # Ajout des 3 checkbuttons de catégories
        self.__frameCheckBtn = Frame(self)
        self.__frameCheckBtn.pack(side = TOP, fill = X, padx = 5, pady = 5)
        self.__varCbTask      = BooleanVar()
        self.__varCbRepetTask = BooleanVar()
        self.__varCbGroupe    = BooleanVar()
        self.__varCbTask.set(     True)
        self.__varCbRepetTask.set(True)
        self.__varCbGroupe.set(   True)

        Checkbutton(self.__frameCheckBtn, text = "Taches", variable = self.__varCbTask, command = self.checkTask).pack(side = LEFT, fill = BOTH, expand = YES)
        Checkbutton(self.__frameCheckBtn, text = "Taches à répétitions", variable = self.__varCbRepetTask, command = self.checkRepetTask).pack(side = LEFT, fill = BOTH, expand = YES)
        Checkbutton(self.__frameCheckBtn, text = "Groupes", variable = self.__varCbGroupe, command = self.checkGroupe).pack(side = LEFT, fill = BOTH, expand = YES)

        # Ajout du binding
        # On fait un after car sinon l'événement se déclanche avant que le texte change dans le combobox
        self.barreRecherche.bind("<Key>", lambda e: self.after(10, lambda: self.filter(name = e.widget.get())))
        self.barreRecherche.bind("<<ComboboxSelected>>", lambda e: self.after(10, lambda: self.filter(name = e.widget.get())))
        self.barreRecherche.bind("<FocusOut>", lambda e: self._chercher(e.widget.get()))
        self.barreRecherche.bind("<Return>", lambda e: self._chercher(e.widget.get()))

        # Zone avec la liste des tâches : # >>> XXX c'est quoi ? >>> (c'était là comme ça) >>> : self._chercher(e.widget.get()))
        self.tree = Treeview(self, columns = ('Statut',), height = 0)
        self.tree.pack(expand = YES, fill = BOTH, side = LEFT)

        # Scrollbar :
        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        # Mise à jour graphique :
        self.redessiner()

    ""
    #############
    # Getters : #
    #############
    ""
    def getPeriodManager(self):
        """
        Getter du periodManager
        @return <PeriodManager>
        """
        return self.__periodManager

    ""
    #####################################
    # Méthodes des checkbuttons globaux #
    #####################################
    ""
    def checkTask(self):
        """
        Méthode qui une fois activé mets toutes les taches
        du statut du checkbutton
        """
        statut = self.__varCbTask.get()
        for s in self.getTaskInTaskEditor():
            if isinstance(s, Task) and s.getNbRep() == 0:
                self.addIt(s, statut)
                # On mets à jours les sous taches si conteneur
                if s.isContainer():
                    for st in s.getSubTasks():
                        self.addIt(st, statut) if st.getNbRep() == 0 else None
        self.redessiner()

    def checkRepetTask(self):
        """
        Méthode qui une fois activé mets toutes les taches à répétitions
        du statut du checkbutton
        """
        statut = self.__varCbRepetTask.get()
        # Parcours à la recherche de toutes les taches a repetitions sauf celles des groupes
        for s in self.getTaskInTaskEditor():
            if isinstance(s, Task) and s.getNbRep() != 0:
                self.addIt(s, statut)
                # On mets à jours les sous taches si conteneur
                if s.isContainer():
                    for st in s.getSubTasks():
                        self.addIt(st, statut) if st.getNbRep() != 0 else None
        self.redessiner()

    def checkGroupe(self):
        """
        Méthode qui une fois activé mets tous les groupe
        du statut du checkbutton
        """
        statut = self.__varCbGroupe.get()
        for s in self.getTaskInTaskEditor():
            # Si c'est un groupe
            if isinstance(s, Groupe):
                # On met à jour le groupe
                self.addIt(s, statut)
                # + toutes ses Taches
                for tache in s.getListTasks():
                    self.addIt(tache, statut)
        self.redessiner()

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def redessiner(self):
        """
        Méthode pour mettre à jour l'affichage du Treeview.
        """
        # On efface tout :
        self.tree.destroy()
        self.scrollbar.destroy()
        self.listTreeItem = []
        # On recrée tout :
        self.tree = Treeview(self, columns = ("visible", "nom"), height = 0)
        self.tree.pack(expand = YES, fill = BOTH, side = LEFT)



        # avec la scrollbar :
        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        # configuration des colonnes
        self.tree.column("#0", width = 0)
        self.tree.column(0,    width = 0)
        self.tree.column(1,    width = 0)

        self.tree.heading("#0", text="Visible")
        self.tree.heading(0,    text="Tache", command = self.tri_statut)
        self.tree.heading(1,    text="Statut", command = self.tri_statut)

        # Position d'insertion (utilisé pour les filtres prioritaires)
        insertPos = 0

        # On ajoute les tâches :
        for indice, t in enumerate(self.getTaskInTaskEditor()):
            pos = END
            # Ajout de la tâche :
            self._ajouterTache(t, indice, "", pos)

        ## Add binding :
        # Le fait d'avoir lesTreeview open/close permet de détecter si on clique sur le '+' ou 'visible'
        self.tree.bind('<<TreeviewOpen>>', lambda e : self.__onClic(e, mode = "open"))
        self.tree.bind('<<TreeviewClose>>', lambda e : self.__onClic(e, mode = "close"))
        self.tree.bind('<<TreeviewSelect>>', lambda e : self.__onClic(e, mode = "select"))
        #self.tree.bind("<Button-1>", self.__onClic)

    def __onClic(self, event = None, mode = None):
        """
        Méthode qui reagit au clic pour activer/désactiver
        l'attribut visible des schedulables
        @param mode : <str> Permet de savoir le type de l'event
        """
        x = self.tree.winfo_pointerx() - self.tree.winfo_rootx()
        y = self.tree.winfo_pointery() - self.tree.winfo_rooty()
        itemId = self.tree.identify_row(y)
        # Si on est pas en "select"
        if mode != "select":
            # On ouvre/ferme et c'est tout
            if mode == "open":
                self.listOpen.append(itemId)
            elif mode == "close":
                self.listOpen.remove(itemId)
            # Redessiner permet de détuire le Treeview et donc d'annuler l'event de selection qui arriverait normalement après
            self.redessiner()
            return
        # Si on clique sur la colone des trucs visibles
        if self.tree.identify_column(x) == "#0":
            # Parcours des taches de premier plan
            for t in self.getTaskInTaskEditor():
                # Si on est la tache et l'id
                if t.id == itemId:
                    self.addIt(t)
                    # On met à jour toutes les soustaches
                    if isinstance(t, Task) and t.isContainer():
                        for st in t.getSubTasks():
                            self.addIt(st, self.listeModify[self.iterScheduModify.index(t)][1])
                    elif isinstance(t, Groupe):
                        for tache in t.getListTasks():
                            self.addIt(tache, self.listeModify[self.iterScheduModify.index(t)][1])
                    break
                # Si on est la tache ou une sous ligne de cette tache
                elif itemId.startswith(t.id):
                    # Si le parent est visible, alors on peut choirir à l'individuel
                    if (t in self.iterScheduModify and self.listeModify[self.iterScheduModify.index(t)][1]) \
                        or (t not in self.iterScheduModify and t.isVisible()):
                        # On regarde les sousTaches
                        if isinstance(t, Task):
                            for st in t.getSubTasks():
                                if st.id == itemId:
                                    self.addIt(st)
                                    break
                        elif isinstance(t, Groupe):
                            for tache in t.getListTasks():
                                if tache.id == itemId:
                                    self.addIt(tache)
                                    break
                    break
            self.redessiner()


    def _ajouterTache(self, displayable, idNum, parent, pos, recursionLevel = 0, **kwargs):
            """
            Ajouter une tâche dans l'arbre.
            @param displayable: le ITaskEditorDisplayable à rajouter
            @param parent: ID de la branche parente
            """
            # Si la tâche n'est pas filtrée
            if displayable.getFilterStateWith(self.FILTRE) >= 0 or recursionLevel > 0: # Ne pas filtrer dans les sous-tâches
                # On défini l'ID du nouveau parent :
                parentNew = parent+"p%s"%idNum
                displayable.id = parentNew

                # On fait la couleur :

                self.tree.tag_configure("Couleur%s"%displayable.getColor(), background = displayable.getColor())
                # + celle de la ligne
                if self.getApplication().getData().testDataExist("General", "Thème", "couleur adaptative") \
                    and self.getApplication().getData().getOneValue("General", "Thème", "couleur adaptative") == "True":
                    self.tree.tag_configure("Couleur%s"%displayable.getColor(), foreground = adaptTextColor(displayable.getColor()))


                # Si le niveau de récursion est trop élevé : on stop.
                if recursionLevel >= 3:
                    self.tree.insert(parent, END, text = str(displayable), values = ["Too Many Recursion"], iid = parentNew,  tags = "Couleur%s"%displayable.getColor())
                    return

                # On insère la ligne d'entête :
                # S'il n'y a pas de changements locaux on prends la valeur de l'attribut
                texte = displayable.isVisible() if displayable not in self.iterScheduModify else self.listeModify[self.iterScheduModify.index(displayable)][1]
                a = self.tree.insert(parent, pos, text = texte, values = displayable.getHeader(), iid = parentNew, tags = ["Couleur%s"%displayable.getColor(), parentNew], open = parentNew in self.listOpen)
                # On rajoute l'iid à la liste
                self.listTreeItem.append(parentNew)

                # On insère les éléments supplémentaires :
                args = {} # *args sont pour la prochaine récursion. **kwargs sont pour l'actuelle.
                lastParentIndex = 0
                for indice, ligne in enumerate(displayable.iterateDisplayContent(**kwargs)):
                    # Si c'est de la récursion : on récursionne.
                    if isinstance(ligne, ITaskEditorDisplayableObject):
                        self._ajouterTache(ligne, indice, parentNew+"e%s"%lastParentIndex, END, recursionLevel+1, **args)
                    # Sinon c'est un élément
                    elif isinstance(ligne, dict):
                        args = ligne
                    else:
                        self.tree.insert(parentNew, END, text=ligne[0], values=[ligne[1]], iid=parentNew+"e%s"%indice, tags=["Couleur%s"%displayable.getColor(), parentNew], open = parentNew+"e%s"%indice in self.listOpen )
                        lastParentIndex = indice
                        # On rajoute l'iid à la liste
                        self.listTreeItem.append(parentNew+"e%s"%indice)

    def addIt(self, tache, mode = None):
        """
        Méthode qui permet d'ajouter la tache à la liste
        des taches dont la visibilité change. Ce qui permet d'enregistrer ça en local
        @param tache : <Task> tache qu'il faut ajouter
        @param mode  : <bool> si on veut set un truc spécial
        """
        # Si ça fait partie de ceux qu'on a déjà modifié
        if tache in self.iterScheduModify:
            self.listeModify[self.iterScheduModify.index(tache)] = [tache, not self.listeModify[self.iterScheduModify.index(tache)][1]] if mode is None else [tache, mode]
        # Sinon on rajoute à ceux qu'on a modifié
        else:
            self.listeModify.append([tache, not tache.isVisible()]) if mode is None else self.listeModify.append([tache, mode])
            self.iterScheduModify.append(tache)
    ""
    ###########
    # onClose #
    ###########
    ""
    def onClose(self, button):
        self.masquage = False
        if button == "Ok":
            # On cherche s'il y a des changements
            for i in range(len(self.iterScheduModify)):
                self.listeModify[i][0].setVisible(self.listeModify[i][1])
            i = 0
            # On cherche s'il y en a un qui est caché
            while not self.masquage and i < len(self.getPeriodManager().getActivePeriode().getPrimitivesSchedulables()):
                s = self.getPeriodManager().getActivePeriode().getPrimitivesSchedulables()[i]
                if not s.isVisible():
                    self.masquage = True
                    break
                if isinstance(s, Task):
                    if s.isContainer():
                        for st in s.getSubTasks():
                            if not st.isVisible():
                                self.masquage = True
                                break
                elif isinstance(s, Groupe):
                    for st in s.getListTasks():
                        if not st.isVisible():
                            self.masquage = True
                            break
                i+=1
        return self.masquage
