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
        """
        # Note : master est une référence vers le dialog
        Frame.__init__(self, master, **kw)

        # Attributs normaux :
        #self.mousepress = False
        self.MODE_TRI = "None"

        self.taches = []
        print(periodManager)
        self.__periodManager = periodManager

#        # Zone pour l'ajouteur des tâches.
#        self.frameInput = TaskAdder(self)
#        self.frameInput.pack(side = TOP, fill = X)

#        self.frameInputPeriode = PeriodAdder(self.getPeriodManager(), self)

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

#        # Ajout du binding
#        # On fait un after car sinon l'événement se déclanche avant que le texte change dans le combobox
#        self.barreRecherche.bind("<Key>", lambda e: self.after(10, lambda: self.filter(name = e.widget.get())))
#        self.barreRecherche.bind("<<ComboboxSelected>>", lambda e: self.after(10, lambda: self.filter(name = e.widget.get())))
#        self.barreRecherche.bind("<FocusOut>", lambda e: self.__chercher(e.widget.get()))
#        self.barreRecherche.bind("<Return>", lambda e: self.__chercher(e.widget.get()))

        # Zone avec la liste des tâches : # >>> XXX c'est quoi ? >>> (c'était là comme ça) >>> : self.__chercher(e.widget.get()))
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

        # Add binding :
        self.tree.bind("<Button-1>", self.__onClic)

    def __onClic(self, event):
        """
        Méthode qui reagit au clic pour activer/désactiver
        l'attribut visible des schedulables
        """
        print("focus")
        a = self.tree.focus()
        print(a)
        #if self.tree.identify_column(event.x) == "#0":
        for t in self.getTaskInTaskEditor():
            print(t.id)
            if t.id == a:
                t.setVisible(not t.isVisible())
                print("setted")
                break
        #self.redessiner()
        return

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
                a = self.tree.insert(parent, pos, text = displayable.isVisible(), values = displayable.getHeader(), iid = parentNew, tags = ["Couleur%s"%displayable.getColor(), parentNew, "rmenu%s"%parentNew])

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
                        self.tree.insert(parentNew, END, text=ligne[0], values=[ligne[1]], iid=parentNew+"e%s"%indice, tags=["Couleur%s"%displayable.getColor(), parentNew])
                        lastParentIndex = indice
    ""
    ###########
    # onClose #
    ###########
    ""
    def onClose(button):
        if button == "Ok":
            print("ok.")
        fen.destroy()

