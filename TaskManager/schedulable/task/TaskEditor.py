# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from collections import deque

from affichages.periode.PeriodAdder import *
from util.widgets.RMenu import *

from .dialog.askHeureExacteDialog import *
from .undoredo.UndoRedoTaskCreation import *
from .Task import *
from .TaskAdder import *
from util.util import adaptTextColor

from ..AbstractSchedulableObject import *

class TaskEditor(Frame):
    """
    Zone à gauche de la fenêtre, dans laquelle sont listée les tâches.
    Contient aussi le widget qui permet d'en rajouter (TaskAdder).
    """
    def __init__(self, master, menubar, periodManager):
        """
        Constructeur du TaskEditor.
        @param master : Référence vers le widget sur lequel on veut le placer.
        @param menubar: Référence vers la barre de menus, pour les design de l'horloge dans TaskAdder.
        @param periodManager: Gestionnaire de périodes, pour l'ajouteur de période.
        """
        Frame.__init__(self, master)
        # Note : master est une référence vers Application
        
        # Attributs normaux :
        self.menu = menubar
        self.mousepress = False
        self.MODE_TRI = "None"

        self.taches = [] # Pourra aussi contenir des Périodes.
        self.__rmenu = [] # Liste des menus clic-droit pour faire que les tâches puissent être transformées en Inconnues.

        # Zone pour l'ajouteur des tâches.
        self.frameInput = TaskAdder(self, menubar)
        self.frameInput.pack(side = TOP, fill = X)
        
        self.frameInputPeriode = PeriodAdder(periodManager, self)

        # Pour pouvoir filtrer l'affichage :
        self.FILTRE = {}
        
        # Zone des recherche :
        self.frameRecherche = Frame(self)
        self.frameRecherche.pack(side = BOTTOM, fill = X)
        Label(self.frameRecherche, text = "Rechercher :").pack(side = LEFT)
        self.barreRecherche = Combobox(self.frameRecherche)
        self.barreRecherche.pack(side = LEFT, fill = X, expand = YES)
        
        # Liste des 10 dernières recherches:
        self.__dernieresRecherches = deque(maxlen=10)
        
        # Ajout du binding
        # On fait un after car sinon l'événement se déclanche avant que le texte change dans le combobox
        self.barreRecherche.bind("<Key>", lambda e: self.after(10, lambda: self.filter(name = e.widget.get())))
        self.barreRecherche.bind("<<ComboboxSelected>>", lambda e: self.after(10, lambda: self.filter(name = e.widget.get())))
        self.barreRecherche.bind("<FocusOut>", lambda e: self.__chercher(e.widget.get()))
        self.barreRecherche.bind("<Return>", lambda e: self.__chercher(e.widget.get()))

        # Zone avec la liste des tâches : # >>> XXX c'est quoi ? >>> (c'était là comme ça) >>> : self.__chercher(e.widget.get()))
        self.tree = Treeview(self, columns = ('Statut',), height = 0)
        self.tree.pack(expand = YES, fill = BOTH, side = LEFT)

        # Scrollbar :
        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        # Mise à jour graphique :
        self.redessiner()

        periodManager.setTaskEditor(self)

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        """
        Getter pour l'application.
        @return l'Application.
        """
        return self.master

    def getPeriodActive(self):
        """
        Getter pour la période active
        @return la période
        """
        return self.getPeriodManager().getActivePeriode()

    def getPeriodManager(self):
        """
        Getter pour le periode manager
        @return le PeriodManager
        """
        return self.getApplication().getPeriodManager()

    def getTaskInTaskEditor(self):
        """
        Getter pour la liste des tâches qui doivent être affiché ou des périodes selon le filtre
        @old : remplace tâches
        @return une liste de schedulable et TaskUnplanified
        """
        if "type" in self.FILTRE and "Période" in self.FILTRE["type"]:
            return self.getPeriodManager().getPeriodes()
        elif self.getPeriodActive():
            return self.getPeriodActive().getPrimitivesSchedulables()
        else:
            return []

    ""
    #############
    # Setters : #
    #############
    ""
    def setEditionPeriode(self, enEdition):
        """
        Permet de changer entre l'ajouteur
        de tâches et l'ajouteur de périodes.
        @param enEdition: True pour l'ajouteur de périodes, False pour l'ajouteur de tâches.
        Note : peut-être changer sur une enumeration généralisée pour pleins de modes d'ajouteurs ?
        (Même si on en fera pas 50, c'est certain.)...
        """
        if enEdition:
            self.frameInput.pack_forget()
            self.frameInputPeriode.pack(side = TOP, fill = X, before = self.tree)
        else :
            self.frameInput.pack(side = TOP, fill = X, before = self.tree)
            self.frameInputPeriode.pack_forget()

    ""
    ###################################
    # Méthodes liées aux schedulables #
    ###################################
    ""
    def __ajouterTache(self, displayable, idNum, parent, pos, recursionLevel = 0, **kwargs):
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
            a = self.tree.insert(parent, pos, text = displayable.getHeader()[0], values = [displayable.getHeader()[1]], iid = parentNew, tags = ["Couleur%s"%displayable.getColor(), parentNew, "rmenu%s"%parentNew])

            # On insère les éléments supplémentaires :
            args = {} # *args sont pour la prochaine récursion. **kwargs sont pour l'actuelle.
            lastParentIndex = 0
            for indice, ligne in enumerate(displayable.iterateDisplayContent(**kwargs)):
                # Si c'est de la récursion : on récursionne.
                if isinstance(ligne, ITaskEditorDisplayableObject):
                    self.__ajouterTache(ligne, indice, parentNew+"e%s"%lastParentIndex, END, recursionLevel+1, **args)
                # Sinon c'est un élément
                elif isinstance(ligne, dict):
                    args = ligne
                else:
                    self.tree.insert(parentNew, END, text=ligne[0], values=[ligne[1]], iid=parentNew+"e%s"%indice, tags=["Couleur%s"%displayable.getColor(), parentNew])
                    lastParentIndex = indice

            # RMenu :
            r = RMenu(self, binder = self.tree, bindWithId = "rmenu%s"%parentNew)
            rmenu = displayable.setRMenuContent(self, r)
            if rmenu:
                self.__rmenu.append(r)
            else:
                # Le try except est nécessaire si jamais ce RMenu() à déjà été détruit dans le displayable.setRMenuContent(self, r)
                try:
                    r.destroy()
                except:
                    pass

    def ajouter(self, iTaskEditorDisplayableObject):
        """
        MÉTHODE À EXÉCUTER PAR LE TaskAdder() ET LE PeriodAdder() UNIQUEMENT !
        Permet d'ajouter un objet affichable dans le TaskEditor.
        @param iTaskEditorDisplayableObject: l'objet à rajouter.
        """
        if isinstance(iTaskEditorDisplayableObject, AbstractSchedulableObject):
            schedulable = iTaskEditorDisplayableObject
            schedulable.getPeriode().addPrimitiveSchedulable(schedulable)   # Ajout primitif
            schedulable.instantiate()                                       # Ajout instancié selon la tâche
            self.getApplication().getDonneeCalendrier().updateAffichage()   # Update
            if isinstance(schedulable, Task):
                task = schedulable
                UndoRedoTaskCreation(self, task)

        self.redessiner()

    def supprimer(self, schedulable):
        """
        MÉTHODE À EXÉCUTER PAR LE RMENU DE SUPPRESSION DU TaskEditor() UNIQUEMENT !
        Permet de supprimer un objet planifiable de la liste.
        @param schedulable: l'objet à enlever.
        """
        if schedulable in self.getTaskInTaskEditor():
            self.getPeriodActive().removePrimitiveSchedulable(schedulable)
        else:
            for s in self.getTaskInTaskEditor():
                if isinstance(s, Task) and s.isContainer():
                    s.removeSubTask(schedulable)
        self.redessiner()

    ""
    ###########################
    # Méthodes liées au tri : #
    ###########################
    ""
    def __chercher(self, text):
        """
        Méthode pour rechercher un texte
        (normalement via la barre de recherche).
        @param text: Le texte cherché.
        """
        text = text.lower().strip()
        self.filter(name = text)
        if text:
            if text in self.__dernieresRecherches:
                self.__dernieresRecherches.remove(text)
            self.__dernieresRecherches.appendleft(text)
        self.barreRecherche.config(values = list(self.__dernieresRecherches))

    def __filterStateOf(self, t):
        """
        Permet de savoir l'état de filtrage d'une tâche.
        @deprecated: Je crois même que ce n'est plus utilisé du tout.
        @return  1 Si la tâche est acceptée par le filtre et qu'elle doit être prioritaire.
        @return  0 Si la tâche est acceptée par le filtre sans être prioritaire.
        @return -1 Si la tâche n'est pas acceptée par le filtre.
        """
        # Filtre prioritaire ?
        if "name" not in self.FILTRE or t.getNom().lower().startswith(self.FILTRE["name"].lower()):
            return 1
        # Filtre normal ?
        elif ("type" not in self.FILTRE or self.FILTRE["type"]=="Tâche") \
         and ("name" not in self.FILTRE or t.getNom().lower().count(self.FILTRE["name"].lower())>0):
            return 0
        # Sinon : non filtré.
        return -1

    def filter(self, **filtre):
        """
        Méthode pour rajouter un filtre.
        @param **filtre: Filtre à mettre.
        Voir dans les objets filtrés (ITaskEditorDisplayableObject#getFilterState()) pour plus d'info.
        """
        for k in filtre:
            k = k.lower()
            if filtre[k]:
                self.FILTRE[k] = filtre[k]
            elif k in self.FILTRE:
                del self.FILTRE[k]
        print(self.FILTRE)
        self.redessiner()

    def tri_alphabetique(self):
        """
        Méthode pour aller sur le prochain
        mode de tri alphabétique.
        """
        if self.MODE_TRI == "Alpha":
            self.MODE_TRI = "Alpha_reverse"
        else:
            self.MODE_TRI = "Alpha"
        self.getTaskInTaskEditor().sort(key=lambda t: t.getNom(), reverse=self.MODE_TRI=="Alpha_reverse")
        self.redessiner()

    def tri_statut(self):
        """
        Méthode pour aller sur le prochain
        mode de tri selon les statuts.
        """
        if self.MODE_TRI == "Statut_importance":
            self.MODE_TRI = "Statut_prochain"
            self.getTaskInTaskEditor().sort(key=lambda t: t.getDebut() if t.getDebut() is not None else datetime.datetime(1, 1, 1))
            self.getTaskInTaskEditor().sort(key=lambda t: 0 if t.getStatut() == "À faire" or t.getStatut() == "Répétition"
                                      else 1 if t.getStatut() == "Inconnu"
                                      else 2)
        elif self.MODE_TRI == "Statut_prochain":
            self.MODE_TRI = "Statut_autre"
            # Alphabétique pout les Inconnus -> tri alphabétique :
            self.getTaskInTaskEditor().sort(key=lambda t: t.getNom())
            # Ne change pas l'ordre des noms des Inconnus
            # car ils ont tous le même début qui est None
            # -> tri par début pour le reste :
            self.getTaskInTaskEditor().sort(key=lambda t: t.getDebut() if t.getDebut() is not None else datetime.datetime(1, 1, 1))
            # Tri selon le statut :
            self.getTaskInTaskEditor().sort(key=lambda t: 0 if t.getStatut() == "Inconnu"
                                      else 1 if t.getStatut() == "Retard"
                                      else 2 if t.getStatut() == "Répétition"
                                      else 3)
        else:
            self.MODE_TRI = "Statut_importance"
            self.getTaskInTaskEditor().sort(key=lambda t: t.getDebut() if t.getDebut() is not None else datetime.datetime(1, 1, 1))
            self.getTaskInTaskEditor().sort(key=lambda t: 0 if t.getStatut() == "Retard"
                                      else 1 if t.getStatut() == "À faire" or t.getStatut() == "Répétition"
                                      else 2)
        self.redessiner()

    ""
    ###################################
    # Méthodes liées au Drag & Drop : #
    ###################################
    ""
    def __mouseDragged(self, event):
        """
        Méthode pour commencer le Drag&Drop d'une tâche.
        @param event: Événement pour positionner la tâche
        en Drag&Drop suivant la position de la souris.
        """
        if self.mousepress:
            self.mousepress = False
            pos = (max(event.x_root - 100, 0), max(event.y_root - 25, 0))
            for i in self.tree.selection(): # Parcourir et obtenir tout les éléments sélectionnés.
                for t in self.getTaskInTaskEditor():
                    if isinstance(t, Task) and t.getStatut() == "Inconnu":
                        if i == t.id:
                            tdnd = TaskInDnd(pos, self, t, command = self.__trouverPositionTache)

    def __mousePressed(self, event):
        """
        Méthode qui ne fait rien.
        @param event: non utilisé.
        """
        pass

    def __mousePressedBefore(self, event):
        """
        Méthode pour quand on sélectionne un truc dans le treeview,
        juste avant qu'il soit réellement sélectionné.
        @param event: infos sur l'évement de sélection.
        """
        self.mousepress = True
        for elem in self.tree.selection():
            self.tree.selection_remove(elem)
        self.after(10, self.__mousePressed, event)

    def __mouseReleased(self, event):
        """
        Méthode pour dire que la souris n'est plus pressée.
        @param event: non utilisé.
        """
        self.mousepress = False

    def __trouverPositionTache(self, tache, x, y):
        """
        Cette méthode doit trouver en fonction des coordonnées x et y par rapport à l'écran,
        où mettre la tâche reçue en argument.
        @param tache: la tâche dont on doit trouver la position.
        @param x: La position en X demandée.
        @param y: La position en Y demandée.
        """
        panneau = self.master.getPanneauActif()
        x -= panneau.winfo_rootx() # transformer les coordonnées pour qu'elles soient relatives au panneau.
        y -= panneau.winfo_rooty()
        if x >= 0 and y >= 0 and x < panneau.winfo_width() and y < panneau.winfo_height(): # s'assurer qu'on est au-dessus du panneau :
            region = panneau.identify_region(x, y)
            minute1 = region.minute
            minute2 = int(round(minute1/5)*5)
            region += datetime.timedelta(minutes = minute2 - minute1)
            region = askHeureExacte(self, region) # Définie dans le dialogue askHeureExacteDialog.py
            if region is not None:
                sousTache = panneau.applyRegion(tache, region)
                if sousTache is not None:
                    # Mise à jour du statut :
                    sousTache.updateStatut()
                    # Ajout de la sous-tâche à la tâche:
                    tache.addSubTask(sousTache)
                    # au calendrier :
                    self.getPeriodManager().getActivePeriode().addInstanciatedSchedulable(sousTache)
                    # update le tout :
                    self.getApplication().getDonneeCalendrier().updateAffichage()
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
        self.__rmenu = []

        # On recrée tout :
        self.tree = Treeview(self, columns = ('Statut',), height = 0)
        self.tree.pack(expand = YES, fill = BOTH, side = LEFT)



        # avec la scrollbar :
        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        # configuration des colonnes
        self.tree.column("#0", width = 0)
        self.tree.column(0,    width = 0)

        # On modifie le nom des colonnes
        if "type" in self.FILTRE and "Tâche" in self.FILTRE["type"]:
            tHeaderFirst = "Tâche"
            tHeaderSecon = "Statut"
        elif "type" in self.FILTRE and "Période" in self.FILTRE["type"]:
            tHeaderFirst = "Période"
            tHeaderSecon = "Statut"
        else :
            tHeaderFirst = tHeaderSecon = ""

        self.tree.heading("#0", text=tHeaderFirst, command = self.tri_alphabetique)
        self.tree.heading(0,    text=tHeaderSecon, command = self.tri_statut)

        # Position d'insertion (utilisé pour les filtres prioritaires)
        insertPos = 0

        # On ajoute les tâches :
        for indice, t in enumerate(self.getTaskInTaskEditor()):
            # Définition de la position prioritaire ou non :
            if self.__filterStateOf(t) == 1:
                pos = insertPos
                insertPos += 1
            else:
                pos = END
            # Ajout de la tâche :
            self.__ajouterTache(t, indice, "", pos)

        # Add binding :
        self.tree.bind("<ButtonPress-1>", self.__mousePressedBefore)
        self.tree.bind_all("ButtonReleased-1>", self.__mouseReleased)
        self.tree.bind("<B1-Motion>", self.__mouseDragged)
