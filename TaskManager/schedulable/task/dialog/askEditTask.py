# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

import datetime

from util.widgets.ColorButton import *
from util.widgets.Dialog import *
from util.widgets.ttkcalendar import *

from .datetimeDialog import *
from schedulable.task.Task import *


def askEditTask(task):
    """
    Dialogue qui édite la tache sur ses paramètres
    @param task : <Task> la tache à modifier
    """
    def onClose(button):
        if button == "OK":
            print("ok")
            return
        fen.destroy()

    def askDebut():
        """
        Permet de demander le début de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        ## demande de la date
        date = askdatetime(False)
        if date is None:
            return
        varDebut = date
        btnDebut.config(text = varDebut if varDebut is not None else "")
        autoSetDuree()

    def askFin():
        """
        Permet de demander la fin de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        # demande de la date
        date = askdatetime(False)
        if date is None:
            return
        varFin = date
        btnFin.config(text = varFin if varFin is not None else "")
        autoSetDuree()

    def autoSetDuree():
        """
        Permet de mettre à jour les widgets de durée de tâche.
        """
        ecart = varFin - varDebut
        varJour.set(ecart.days)
        varHour.set(ecart.seconds//3600)
        varMin.set(ecart.seconds//60%60)

    def autoSetFin():
        """
        Fonction qui change automatiquement la fin si on change la durée
        """
        nonlocal varJour, varHour, varMin, btnFin
        varFin = (varDebut + datetime.timedelta(days = varJour.get(), hours = varHour.get(), minutes = varMin.get()))
        btnFin.config(text = varFin)

    fen = Dialog(title = "Édition de \"%s\""%task.getNom(), buttons = ("Ok", "Annuler"), command = onClose)

    def getListTask(list, StringV = False):
        """
        Fonction qui retourne un texte avec toutes les taches de la liste
        @format : Task -- uniqueId (+\n)
        @param list : <list> de task
        @param StringV : <bool> doit-on retourner un stringVar de listbox ?
        @return <str>
        """
        text = ""
        print(list)
        for task in list:
            text += str(task) + "\n\tID : " + task.getUniqueID() + "\n\\"
        if not StringV:
            return text.replace("\\", "")
        else:
            sv = StringVar()
            text = text.replace("\n", "")
            sv.set(text.replace("\t", "   ").split("\\")[:-1])
            return sv

    def supprimeLien(mode):
        """
        Fonction qui supprime un lien
        @param mode : <str> sert a savoir si c'est dépendances ou dépendantes
        """
        def chercheTask(id):
            """
            Fonction embarquée qui recherche la tache lié à l'id
            Pour l'instant seule les task ont un UUID
            @param id : <str> id de la tache qu'on cherche
            @param p  : <periode> celle qui contient la tache
            @return <task> recherché, None si non trouvé
            """
            for t in task.getPeriode().getPrimitivesSchedulables():
                if isinstance(t, Task):
                    if id == t.getUniqueID():
                        return t
                    elif t.isContainer():
                        for st in t.getSubTasks():
                            if st.getUniqueID() == id:
                                return st
        if mode == "depces":
            t = lbListDepces.get(ACTIVE)
            id = t.split("ID")[-1]
            id = id[id.rfind(" ")+1:]
            depces = chercheTask(id)
            deptes = task
        elif mode == "deptes":
            t = lbListDeptes.get(ACTIVE)
            id = t.split("ID")[-1]
            id = id[id.rfind(" ")+1:]
            deptes = chercheTask(id)
            depces = task
        else:
            return
        # On retire la dépendances
        deptes.removeDependance(depces)
        # On met à jour l'affichage
        if mode == "depces":
            lbListDepces.config(listvariable = getListTask(task.getDependances(), StringV = True))
        elif mode == "deptes":
            lbListDeptes.config(listvariable = getListTask(task.getDependantes(), StringV = True))


    # Variable modifiable
    varNom = StringVar()
    varPeriode = StringVar()
    varCouleur = StringVar()
    # textDesc (je le met ici pour ne pas l'oublier)
    varDebut = "" # Initialisation, affectation après
    varFin = ""
    varDuree = None
    varJour = IntVar()
    varHour = IntVar()
    varMin = IntVar()
    varNbRep = IntVar()
    varRepTimedelta = None
    varRep = IntVar()
    varUnitRep = StringVar()
    varID = StringVar()
    varDone = BooleanVar()


    # Affectation des variables
    varNom.set(task.getNom())
    varPeriode.set(task.getPeriode().getNom())
    varCouleur.set(task.getColor())
    # textDesc (je le met ici pour ne pas l'oublier)
    varDebut = task.getDebut()
    varFin = task.getFin()
    varDuree = task.getDuree()
    varJour.set(varDuree.days)
    varHour.set(varDuree.seconds//3600)
    varMin.set(varDuree.seconds//60%60)
    varNbRep.set(8)
    varRepTimedelta = task.getRep() if task.getRep() is not None else datetime.timedelta()
    varRep = varRepTimedelta.seconds//3600 if varRepTimedelta.days == 0 else varRepTimedelta.days
    if varRep == 0: # ici les heures valent 0
        varUnitRep.set("jours")
    elif varRepTimedelta.days == 0 and varRep != 0:
        varUnitRep.set("heures")
    elif varRepTimedelta.days % 7 == 0:
        varUnitRep.set("semaines")
    else:
        varUnitRep.set("jours")
    varID.set(task.getUniqueID())
    varDone.set(task.isDone())

    ## Notebook
    nb = Notebook(fen)
    pageGeneral = Frame(nb)
    pageAvancee = Frame(nb)
    nb.add(pageGeneral, text = "Général")
    nb.add(pageAvancee, text = "Avancée")

    ## Attributs généraux
    frameGeneral = LabelFrame(pageGeneral, text = "Attributs généraux")
    lbNom        = Label(      frameGeneral, text = "Nom :")
    entryNom     = Entry(      frameGeneral, textvariable = varNom)
    lbPeriode    = Label(      frameGeneral, text = "Période :")
    comboPeriode = Combobox(   frameGeneral, textvariable = varPeriode, value = [p.getNom() for p in task.getApplication().getPeriodManager().getPeriodes()])
    lbColor      = Label(      frameGeneral, text = "Couleur :")
    colbut       = ColorButton(frameGeneral, bg = varCouleur.get())
    lbDesc       = Label(      frameGeneral, text = "Description :")
    textDesc     = Text(       frameGeneral, wrap = "word", height = 3, width = 30)
    textDesc.insert(END, task.getDescription()) # Car on peut pas mettre de variable
    sep = Separator(frameGeneral, orient = HORIZONTAL)
    lbDebut = Label(frameGeneral, text = "Début :")
    btnDebut = Button(frameGeneral, text = varDebut, command = askDebut)
    lbFin = Label(frameGeneral, text = "Fin :")
    btnFin = Button(frameGeneral, text = varFin, command = askFin)
    lbDuree = Label(frameGeneral, text = "Durée :")
    # Duree
    frameDuree = Frame(frameGeneral)
    sbJour = Spinbox(frameDuree, from_ = 0, to=31, increment = 1, width = 4, textvariable = varJour, command = autoSetFin)
    lbJour = Label(frameDuree, text = "jours")
    sbHour = Spinbox(frameDuree, from_ = 0, to=23, increment = 1, width = 4, textvariable = varHour, command = autoSetFin)
    lbHour = Label(frameDuree, text = "heures")
    sbMin = Spinbox(frameDuree, from_ = 0, to=59, increment = 1, width = 4, textvariable = varMin, command = autoSetFin)
    lbMin= Label(frameDuree, text = "minutes")
    # Répétition
    lbNbRep = Label(frameGeneral, text = "Nombre de répétitions :")
    sbNbRep = Spinbox(frameGeneral, from_ = -1, to = 100, increment = 1, width = 4, textvariable = varNbRep)
    lbRepet = Label(frameGeneral, text = "Fréquence :")
    frameRepet = Frame(frameGeneral)
    sbRep = Spinbox(frameRepet, from_ = 1, to = 100, increment = 1, width = 4, textvariable = varRep)
    cbUnit = Combobox(frameRepet, value = ["semaine", "jours", "heures"], textvariable = varUnitRep)

    ## Attributs avancés
    frameAdvanced = LabelFrame(pageAvancee, text = "Options avancées")
    lbId = Label(frameAdvanced, text = "ID :")
    entryId = Entry(frameAdvanced, textvariable = varID, state = DISABLED)
    lbSubtask = Label(frameAdvanced, text = "Sous-tâches :")
    lbListSub = Label(frameAdvanced, text = getListTask(task.getSubTasks()) if task.isContainer() else "Tache non conteneur", anchor = "nw")
    lbDepces = Label(frameAdvanced, text = "Dépendances :")
    lbListDepces = Listbox(frameAdvanced, listvariable = getListTask(task.getDependances(), StringV = True), selectmode = "single", height = len(getListTask(task.getDependances(), StringV = True).get().split("\\")))
    btnSupprDepces = Button(frameAdvanced, text = "Supprimer", command = lambda : supprimeLien("depces"))
    lbDeptes = Label(frameAdvanced, text = "Dépendantes :")
    lbListDeptes = Listbox(frameAdvanced, listvariable = getListTask(task.getDependantes(), StringV = True), selectmode = "single", height = len(getListTask(task.getDependantes(), StringV = True).get().split("\\")))
    btnSupprDeptes = Button(frameAdvanced, text = "Supprimer", command = lambda : supprimeLien("deptes"))
    lbDone = Label(frameAdvanced, text = "Fait :")
    cbDone = Checkbutton(frameAdvanced, variable = varDone)
    lbParent = Label(frameAdvanced, text = "Parent :")
    lbResultParent = Label(frameAdvanced, text = task.getParent() if task.getParent() else "")


    

    ## Affichage
    nb.pack(fill = BOTH, expand = YES)
    # Général
    frameGeneral.pack(side = TOP, fill = BOTH, expand = YES)
    lbNom.grid(       row = 0, column = 0, sticky = "e")
    entryNom.grid(    row = 0, column = 1, sticky = "we")
    lbPeriode.grid(   row = 1, column = 0, sticky = "e")
    comboPeriode.grid(row = 1, column = 1, sticky = "we")
    lbColor.grid(     row = 2, column = 0, sticky = "e")
    colbut.grid(      row = 2, column = 1)
    lbDesc.grid(      row = 3, column = 0, sticky = "e")
    textDesc.grid(    row = 4, column = 0, sticky = "we", columnspan = 2)
    sep.grid(         row = 5, column = 0, sticky = "we", columnspan = 2, pady = 2)
    lbDebut.grid(     row = 6, column = 0, sticky = "e")
    btnDebut.grid(    row = 6, column = 1, sticky = "we")
    lbFin.grid(       row = 7, column = 0, sticky = "e")
    btnFin.grid(      row = 7, column = 1, sticky = "we")
    # Duree
    lbDuree.grid(     row = 8, column = 0, sticky = "e")
    frameDuree.grid(  row = 8, column = 1, sticky = "we")
    sbJour.grid(      row = 0, column = 0)
    lbJour.grid(      row = 0, column = 1)
    sbHour.grid(      row = 0, column = 2)
    lbHour.grid(      row = 0, column = 3)
    sbMin.grid(       row = 0, column = 4)
    lbMin.grid(       row = 0, column = 5)
    lbNbRep.grid(row = 9, column = 0, sticky = "e")
    frameRepet.grid(row = 9, column = 1, sticky = "we")
    sbRep.pack(side = LEFT, fill = BOTH)
    cbUnit.pack(side = LEFT, fill = BOTH, expand = YES)
    # Avancée
    frameAdvanced.pack(side = TOP, fill = BOTH, expand = YES)
    lbId.grid(        row = 0, column = 0, sticky = "e")
    entryId.grid(     row = 0, column = 1, sticky = "we")
    lbSubtask.grid(   row = 1, column = 0, sticky = "e")
    lbListSub.grid(   row = 1, column = 1, sticky = "w")
    lbDepces.grid(    row = 2, column = 0, sticky = "ne")
    lbListDepces.grid(row = 2, column = 1, sticky = "nswe", rowspan = 2)
    btnSupprDepces.grid( row = 3, column = 0, sticky = "e")
    lbDeptes.grid(    row = 4, column = 0, sticky = "ne")
    lbListDeptes.grid(row = 4, column = 1, sticky = "nswe", rowspan = 2)
    btnSupprDeptes.grid( row = 5, column = 0, sticky = "e")
    lbDone.grid(row = 6, column = 0, sticky = "e")
    cbDone.grid(row = 6, column = 1, sticky = "we")
    lbParent.grid(row = 7, column = 0, sticky = "e")
    lbResultParent.grid(row = 7, column = 1, sticky = "w")

    # Config grid
    frameAdvanced.columnconfigure(1, weight = 1)




    autoSetDuree()
    fen.activateandwait()


def creeTask(dict):
    """
    Fonction qui supprime puis crée la tache une fois les opérrations faites
    """
    pass
