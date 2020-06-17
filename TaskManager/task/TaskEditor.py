# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from collections import deque

from affichages.periode.PeriodAdder import *
from util.widgets.Dialog import *
from util.widgets.RMenu import *

from .Task import *
from .TaskAdder import *

class TaskEditor(Frame):
    """
    Zone à gauche de la fenêtre, dans laquelle sont listée les tâches.
    Contient aussi le widget qui permet d'en rajouter (TaskAdder).
    """
    def __init__(self, master, menubar, periodManager):
        """
        @param master : Référence vers le widget sur lequel on veut le placer.
        @param menubar: Référence vers la barre de menus, pour les design de l'horloge dans TaskAdder.
        """
        Frame.__init__(self, master, bg="red")
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

        # Zone avec la liste des tâches : self.__chercher(e.widget.get()))
        self.tree = Treeview(self, columns = ('Statut',), height = 0)
        self.tree.pack(expand = YES, fill = BOTH, side = LEFT)

        # Scrollbar :
        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tree.configure(yscrollcommand = self.scrollbar.set)
        
        # Mise à jour graphique :
        self.redessiner()

        periodManager.setTaskEditor(self)

    def filter(self, **filtre):
        """
        Méthode pour rajouter un filtre.
        """
        for k in filtre:
            k = k.lower()
            if filtre[k]:
                self.FILTRE[k] = filtre[k]
            elif k in self.FILTRE:
                del self.FILTRE[k]
        print(self.FILTRE)
        self.redessiner()
    
    def __chercher(self, text):
        text = text.lower().strip()
        self.filter(name = text)
        if text:
            if text in self.__dernieresRecherches:
                self.__dernieresRecherches.remove(text)
            self.__dernieresRecherches.appendleft(text)
        self.barreRecherche.config(values = list(self.__dernieresRecherches))
        
    def ajouter(self, tache):
        self.taches.append(tache)
        self.redessiner()
        if isinstance(tache, Task) and tache.statut != "Inconnu":
            self.master.getDonneeCalendrier().addTask(tache)
        self.frameInput.updatePossiblePeriods()
    def supprimer(self, tache):
        self.taches.remove(tache)
        self.redessiner()
        if isinstance(tache, Task) and tache.statut != "Inconnu":
            self.master.getDonneeCalendrier()#.removeTask(tache) # TODO
        self.frameInput.updatePossiblePeriods()

    def redessiner(self):
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

        # configuration des colones
        self.tree.column("#0", width = 0)
        self.tree.column(0,    width = 0)
        self.tree.heading("#0", text="Tâche", command = self.tri_alphabetique)
        self.tree.heading(0,    text="Statut", command = self.tri_statut)
        
        # Position d'insertion (utilisé pour les filtres prioritaires)
        insertPos = 0

        # On ajoute les tâches :
        for indice, t in enumerate(self.taches):
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

            # Si le niveau de récursion est trop élevé : on stop.
            if recursionLevel >= 3:
                self.tree.insert(parent, END, text = str(displayable), values = ["Too Many Recursion"], iid = parentNew,  tags = "Couleur%s"%displayable.getColor())
                return

            # On insère la ligne d'entête :
            self.tree.insert(parent, pos, text = displayable.getHeader()[0], values = [displayable.getHeader()[1]], iid = parentNew, tags = ["Couleur%s"%displayable.getColor(), parentNew, "rmenu%s"%parentNew])
            
            # On insère les éléments supplémentaires :
            args = {} # args sont pour la prochaine récursion. kwargs sont pour l'actuelle.
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
            self.__rmenu.append(r)
            rmenu = displayable.getRMenuContent(self, r)
            if rmenu is not None:
                for type, kwargs in rmenu:
                    if type == "command":
                        func = r.add_command
                    elif type=="cascade":
                        func = r.add_cascade
                    elif type=="checkbutton":
                        func = r.add_checkbutton
                    elif type=="radiobutton":
                        func = r.add_radiobutton
                    elif type=="separator":
                        func = r.add_separator
                    else:
                        r.destroy()
                        self.__rmenu.remove(r)
                        raise ValueError("Got an invalide keyword for rmenu for the TaskEditor's Treeview: %s"%type)
                    func(**kwargs)
            else:
                self.__rmenu.remove(r)
                r.destroy()
    
    def __filterStateOf(self, t):
        """
        @return  1 Si la tâche est acceptée par le filtre et qu'elle doit être prioritaire.
        @return  0 Si la tâche est acceptée par le filtre sans être prioritaire.
        @return -1 Si la tâche n'est pas accetpée par le filtre.
        """
        # Filtre prioritaire ?
        if "name" not in self.FILTRE or t.nom.lower().startswith(self.FILTRE["name"].lower()):
            return 1
        # Filtre normal ?
        elif ("type" not in self.FILTRE or self.FILTRE["type"]=="Tâche") \
         and ("name" not in self.FILTRE or t.nom.lower().count(self.FILTRE["name"].lower())>0):
            return 0
        # Sinon : non filtré.
        return -1

    def __mouseReleased(self, event):
        self.mousepress = False
    def __mousePressedBefore(self, event):
        self.mousepress = True
        for elem in self.tree.selection():
            self.tree.selection_remove(elem)
        self.after(10, self.__mousePressed, event)
    def __mousePressed(self, event):
        pass
    def __mouseDragged(self, event):
        if self.mousepress:
            self.mousepress = False
            pos = (max(event.x_root - 100, 0), max(event.y_root - 25, 0))
            for i in self.tree.selection(): # Parcourir et obtenir tout les éléments sélectionnés.
                print(i)
                print(self.tree.item(i))
                for t in self.taches:
                    if isinstance(t, Task) and t.statut == "Inconnu":
                        print(i)
                        if i == t.id:
                            tdnd = TaskInDnd(pos, self, t, command = self.__trouverPositionTache)
    def __trouverPositionTache(self, tache, x, y):
        """
        Cette méthode doit trouver en fonction des coordonnées x et y par rapport à l'écran,
        où mettre la tâche reçue en argument.
        """
        panneau = self.master.getPanneauActif()
        x -= panneau.winfo_rootx() # transformer les coordonnées pour qu'elles soient relatives au panneau.
        y -= panneau.winfo_rooty()
        if x >= 0 and y >= 0 and x < panneau.winfo_width() and y < panneau.winfo_height(): # s'assurer qu'on est au-dessus du panneau :
            region = panneau.identify_region(x, y)
            minute1 = region.minute
            print("region avant :", region)
            minute2 = int(round(minute1/5)*5)
            region += datetime.timedelta(minutes = minute2 - minute1)
            print("region après :", region)
            region = self.__askHeureExacte(region)
            if region is not None:
                sousTache = panneau.addTask(tache, region = region)
                for p in self.master.getDonneeCalendrier().getToutLesPanneaux():
                    if p != panneau:
                        p.addTask(sousTache, region)
                sousTache.updateStatut()
                tache.addSubTask(sousTache)
                self.redessiner()
    
    def __askHeureExacte(self, region):
        heure1 = region.hour
        minute1 = region.minute
        def onClose(bouton):
            nonlocal region
            if bouton == "Reset":
                h.set(heure1)
                m.set(minute1)
                return
            if bouton == "Ok":
                heure2 = int(h.get())
                minute2 = int(m.get())
                region += datetime.timedelta(minutes = heure2*60 - heure1 * 60 + minute2 - minute1)
            else:
                region = None
            fen.destroy()
        def minutePres():
            if var.get():
                m.config(increment = 1)
            else:
                m.config(increment = 5)
        def adapteHeure():
            """Adapte les heures quand on augmente (ou diminue) trop les minutes."""
            minutes = int(m.get())
            heures = int(h.get())
            while minutes < 0:
                minutes += 60
                heures -= 1
            while minutes >= 60:
                minutes -= 60
                heures += 1
            heures += 24
            heures %= 24
            m.set(minutes)
            h.set(heures)

        fen = Dialog(self, "Confirmez l'heure exacte", ("Ok", "Annuler", "Reset"), command = onClose)
        Label(fen, text = "Veuillez entrer l'heure exacte").pack(side = TOP, expand = YES, fill = BOTH)
        var = BooleanVar(value = False)
        c = Checkbutton(fen, text = "Précision à la minute près ?", command = minutePres, variable = var)
        c.pack(side = TOP, fill = X)
        Label(fen, text = "Heure :").pack(side = LEFT)
        h = Spinbox(fen, from_ = -1, to = 24, increment = 1, command = adapteHeure)
        h.pack(side = LEFT, fill = X, expand = YES)
        m = Spinbox(fen, from_ = -5, to = 64, increment = 5, command = adapteHeure)
        m.pack(side = RIGHT, fill = X, expand = YES)
        Label(fen, text = "Minute :").pack(side = RIGHT)
        onClose("Reset")
        fen.activateandwait()
        return region

    def getApplication(self):
        return self.master
    def tri_alphabetique(self):
        if self.MODE_TRI == "Alpha":
            self.MODE_TRI = "Alpha_reverse"
        else:
            self.MODE_TRI = "Alpha"
        self.taches.sort(key=lambda t: t.nom, reverse=self.MODE_TRI=="Alpha_reverse")
        self.redessiner()
    def tri_statut(self):
        if self.MODE_TRI == "Statut_importance":
            self.MODE_TRI = "Statut_prochain"
            self.taches.sort(key=lambda t: t.debut if t.debut is not None else datetime.datetime(1, 1, 1))
            self.taches.sort(key=lambda t: 0 if t.statut == "À faire" or t.statut == "Répétition"
                                      else 1 if t.statut == "Inconnu"
                                      else 2)
        elif self.MODE_TRI == "Statut_prochain":
            self.MODE_TRI = "Statut_autre"
            # Alphabétique pout les Inconnus -> tri alphabétique :
            self.taches.sort(key=lambda t: t.nom)
            # Ne change pas l'ordre des noms des Inconnus
            # car ils ont tous le même debut qui est None
            # -> tri par début pour le reste :
            self.taches.sort(key=lambda t: t.debut if t.debut is not None else datetime.datetime(1, 1, 1))
            # Tri selon le statut :
            self.taches.sort(key=lambda t: 0 if t.statut == "Inconnu"
                                      else 1 if t.statut == "Retard"
                                      else 2 if t.statut == "Répétition"
                                      else 3)
        else:
            self.MODE_TRI = "Statut_importance"
            self.taches.sort(key=lambda t: t.debut if t.debut is not None else datetime.datetime(1, 1, 1))
            self.taches.sort(key=lambda t: 0 if t.statut == "Retard"
                                      else 1 if t.statut == "À faire" or t.statut == "Répétition"
                                      else 2)
        self.redessiner()
    
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