# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label


from util.widgets.Dialog import *
from util.util import adaptDatetime, datetimeToStr

def askSeparateRepetitiveTask(task):
    """
    Dialogue qui gère les taches à répétitions (les jours à ne pas afficher et autres
    @param task : <Task> tache dont on gère les répétition
    """
    from ..Task import Task

    def onClose(button):
        if button == "Ok":
            print("ok.")

    def makeListDissociated():
        """
        Fonction qui génère la liste des répétition avec un jolie texte
        @return <list> un truc parfait pour le StringVar de la listeDate
        """
        listTemp = [] # variable temporaire pour améliorer la visibilité
        for numero in range(task.getNbRep()):
            if numero in task.getDissociated(): # on rajoute * si dissocié
                listTemp.append("*" + adaptDatetime(numero*task.getRep() + task.getDebut()))
            else :
                listTemp.append(adaptDatetime(numero*task.getRep() + task.getDebut()))
        return listTemp

    def manageOption(e = None):
        """
        Fonction qui gère les options des boutons
        Active/désactive scinder (on ne peut pas scinder le 1 jour de la répétition)
        Dissocier/associer en fonction de si la répétition à été dissocié ou pas
        @param e : <tkinter.event> inutilisé
        """
        selected = listBoxRepet.curselection()
        # Scinder
        if 1 in selected :
            btnScinder.config(state = DISABLED)
        else:
            btnScinder.config(state = ACTIVE)

        # Dissocier
        # Permet d'avoir accès à l'index sinon c'est un tuple
        for index in selected:
            if index in task.getDissociated():
                # La tache est dissocié, on peut donc la rassocier
                btnSeparate.config(text = "Associer", command = associate, state = ACTIVE)
            else:
                # La tache est dans la liste de répétition, on peut donc l'associer
                btnSeparate.config(text = "Dissocier", command = dissociate, state = ACTIVE)

    def scinder():
        """
        Fonction qui scinde la répétition en une nouvelle répétition à partir
        de la répétition selectionné
        """
        selected = listBoxRepet.curselection()

    def associate():
        """
        Fonction qui remet la tache à répétition dans celles à faire
        En pratique, retire l'itération en question de la liste "setDissociated"
        """
        selected = listBoxRepet.curselection()
        for iteration in selected:
            task.removeDissociated(iteration)

        # On met à jour la liste
        manageOption()
        listeDate.set(makeListDissociated())

    def dissociate():
        """
        Fonction qui ajoute une répétition à ne pas faire
        + crée une autre tache à la date ou la précédante est annulé
        """
        selected = listBoxRepet.curselection()
        # Parcours du tuple pour avoir l'index de la ligne
        for iteration in selected:
            task.addDissociated(iteration)
            ## On créer une nouvelle tache à la place
            dico = task.saveByDict()
            # On retire les répétitions et on met la date de l'itération retiré
            dico["rep"] = "1-0"
            dico["nbrep"] = 0
            periode = task.getPeriode()
            # on change le début
            dico["debut"] = datetimeToStr(task.getDebut() + iteration * task.getRep())

            ## On créer finalement notre nouvelle tache
            newTask = Task.load(dico, periode)
            newTask.setUniqueID()
            # S'il y a une tache parente, on la rajoute en subtask tant qu'a faire
            if dico["parent"] is not None:
                task.getParent().addSubTask(newTask)
                newTask.instantiate()
            # Sinon on la rajoute à la période
            else:
                periode.addPrimitiveSchedulable(newTask)

            # On met à jour la liste
            manageOption()
            listeDate.set(makeListDissociated())

    # Variable
    listeDate = StringVar()

    # Affctation
    listeDate.set(makeListDissociated())

    fen = Dialog(title = "Répétition de \"%s\""%task.getNom(), buttons = ("Ok", "Annuler"), exitButton = ("Ok", "Annuler", "WM_DELETE_WINDOW"), command = onClose)

    # Liste de widget
    lbTop = Label(fen, text = "Gestion des répétitions :\n\t- (*)Dissocier : retire une tache des répétition\n\t- Scinder : crée une nouvelle tache à répétition", justify = LEFT)
    listBoxRepet = Listbox(fen, listvariable = listeDate, selectmode = "single")
    listBoxRepet.bind("<<ListboxSelect>>", manageOption) # Bind associé
    frameBtn = Frame(fen)
    btnSeparate = Button(frameBtn, text = "Dissocier", state = DISABLED) # Pour les commandes, voir manageOption
    btnScinder = Button(frameBtn, text = "Scinder", command = scinder, state = DISABLED) # Pour l'état voir manageOption

    # Affichage
    lbTop.grid(row = 0, column = 0, columnspan = 2)
    listBoxRepet.grid(row = 1, column = 0, sticky = "we", padx = 3)
    frameBtn.grid(row = 1, column = 1, sticky = "nsew")
    btnSeparate.grid(row = 0, column = 0, sticky = "we")
    btnScinder.grid(row = 1, column = 0, sticky = "we")

    fen.activateandwait()

