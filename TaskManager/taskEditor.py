# -*- coding:utf-8 -*-
from task import *
from dialog import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame


class TaskEditor(Frame):
    def __init__(self, master, menubar):
        Frame.__init__(self, master, bg="red")
        # Note : master est une référence vers Application
        self.menu = menubar

        self.taches = [] # Pourra aussi contenir des Périodes.

        self.mousepress = False

        self.frameInput = TaskAdder(self, menubar)
        self.frameInput.pack(side = TOP, fill = X)

        self.FILTRE = {}
        self.frameRecherche = Frame(self)
        self.frameRecherche.pack(side = BOTTOM, fill = X)
        Label(self.frameRecherche, text = "Rechercher :").pack(side = LEFT)
        self.barreRecherche = Combobox(self.frameRecherche)
        self.barreRecherche.pack(side = LEFT, fill = X, expand = YES)
        # On fait un after car sinon l'événement se déclanche avant que le texte change dans le combobox
        self.barreRecherche.bind("<Key>", lambda e: self.after(10, lambda: self.filter(name = e.widget.get())))
        self.barreRecherche.bind("<<ComboboxSelected>>", lambda e: self.after(10, lambda: self.filter(name = e.widget.get())))

        self.tree = Treeview(self, columns = ('Statut',), height = 0)
        self.tree.pack(expand = YES, fill = BOTH, side = LEFT)

        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tree.configure(yscrollcommand = self.scrollbar.set)
        
        self.MODE_TRI = "None"

        self.redessiner()

    def filter(self, **filtre):
        for k in filtre:
            if filtre[k]:
                self.FILTRE[k] = filtre[k]
            elif k in self.FILTRE:
                del self.FILTRE[k]
        print(self.FILTRE)
        self.redessiner()

    def ajouter(self, tache):
        self.taches.append(tache)
        self.redessiner()
        if tache.statut != "Inconnu":
            self.master.getDonneeCalendrier().addTask(tache)
    def redessiner(self):
        self.tree.destroy()
        self.scrollbar.destroy()
        self.tree = Treeview(self, columns = ('Statut',), height = 0)
        self.tree.pack(expand = YES, fill = BOTH, side = LEFT)

        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        # configuration des colones
        self.tree.column("#0", width = 0)
        self.tree.column(0,    width = 0)
        self.tree.heading("#0", text="Tâche", command = self.tri_alphabetique)
        self.tree.heading(0,    text="Statut", command = self.tri_statut)

        self.NEW_ID = 0
        insertPos = 0
        for t in self.taches:
            if ("type" not in self.FILTRE or self.FILTRE["type"]=="Tâche") \
            and("name" not in self.FILTRE or t.nom.lower().count(self.FILTRE["name"].lower())>0):
                pos = END
                if "name" not in self.FILTRE or t.nom.lower().startswith(self.FILTRE["name"].lower()):
                    pos = insertPos
                    insertPos += 1
                t.id = self.NEW_ID
                self.tree.insert("", pos, text = t.nom, values = [t.statut], iid = "p%s"%self.NEW_ID, tags = "Couleur%s"%t.color) # p comme parent
                self.tree.insert("p%s"%self.NEW_ID, END, text = "Début :", values = [t.debut], iid = "p%se1"%self.NEW_ID, tags = "Couleur%s"%t.color) # e comme enfant.
                self.tree.insert("p%s"%self.NEW_ID, END, text = "Durée :", values = [t.duree], iid = "p%se2"%self.NEW_ID, tags = "Couleur%s"%t.color)
                self.tree.insert("p%s"%self.NEW_ID, END, text = "Fin :", values = [(t.debut + t.duree) if t.debut is not None else None], iid = "p%se3"%self.NEW_ID, tags = "Couleur%s"%t.color)
                self.tree.insert("p%s"%self.NEW_ID, END, text = "Description :", values = [t.desc], iid = "p%se4"%self.NEW_ID, tags = "Couleur%s"%t.color)
                self.tree.insert("p%s"%self.NEW_ID, END, text = "Nombre rep :", values = [t.nbrep], iid = "p%se5"%self.NEW_ID, tags = "Couleur%s"%t.color)
                self.tree.insert("p%s"%self.NEW_ID, END, text = "temps entre rep :", values = [t.rep], iid = "p%se6"%self.NEW_ID, tags = "Couleur%s"%t.color)
                self.tree.insert("p%s"%self.NEW_ID, END, text = "Dépendences", values = [t.dependences], iid = "p%se7"%self.NEW_ID, tags = "Couleur%s"%t.color)
                self.NEW_ID += 1
                self.tree.tag_configure("Couleur%s"%t.color, background = t.color)

        # Add binding :
        self.tree.bind("<ButtonPress-1>", self.__mousePressedBefore)
        self.tree.bind_all("ButtonReleased-1>", self.__mouseReleased)
        self.tree.bind("<B1-Motion>", self.__mouseDragged)
    def __mouseReleased(self, event):
        self.mousepress = False
    def __mousePressedBefore(self, event):
        self.mousepress = True
        for i in range(self.NEW_ID):
            self.tree.selection_remove("p%s"%i)
            self.tree.selection_remove("p%se1"%i)
            self.tree.selection_remove("p%se2"%i)
            self.tree.selection_remove("p%se3"%i)
            self.tree.selection_remove("p%se4"%i)
            self.tree.selection_remove("p%se5"%i)
            self.tree.selection_remove("p%se6"%i)
            self.tree.selection_remove("p%se7"%i)
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
                    if t.statut == "Inconnu":
                        if i == "p%s"%t.id:
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
                tache = panneau.addTask(tache, region = region)
                for p in self.master.getDonneeCalendrier().getToutLesPanneaux():
                    if p != panneau:
                        p.addTask(tache, region)
                tache.updateStatut()
                self.ajouter(tache)
    
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
        fen = Dialog(self, "Confirmez l'heure exacte", ("Ok", "Annuler", "Reset"), command = onClose)
        Label(fen, text = "Veuillez entrer l'heure exacte").pack(side = TOP, expand = YES, fill = BOTH)
        var = BooleanVar(value = False)
        c = Checkbutton(fen, text = "Précision à la minute près ?", command = minutePres, variable = var)
        c.pack(side = TOP, fill = X)
        Label(fen, text = "Heure :").pack(side = LEFT)
        h = Spinbox(fen, from_ = 0, to = 23, increment = 1)
        h.pack(side = LEFT, fill = X, expand = YES)
        m = Spinbox(fen, from_ = 0, to = 59, increment = 5)
        m.pack(side = RIGHT, fill = X, expand = YES)
        Label(fen, text = "Minute :").pack(side = RIGHT)
        onClose("Reset")
        fen.activateandwait()
        return region

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


if __name__=='__main__':
    import Application
    Application.main()
