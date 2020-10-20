# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.Dialog import *

def askSeparateRepetitiveTask(task):
    """
    Dialogue qui gère les taches à répétitions (les jours à ne pas afficher et autres
    @param task : <Task> tache dont on gère les répétition
    """
    def onClose(button):
        if button == "Ok":
            print("ok.")

    # Variable
    listeDate = StringVar()

    # Affctation
    listeDate.set([numero*task.getRep() + task.getDebut() for numero in range(task.getNbRep())])


    fen = Dialog(title = "Répétition de \"%s\""%task.getNom(), buttons = ("Ok", "Annuler"), exitButton = ("Ok", "Annuler", "WM_DELETE_WINDOW"), command = onClose)

    # Liste de widget
    lbTop = Label(fen, text = "Gestion des répétitions :\n\t- Dissocier : retire une tache des répétition\n\t- Scinder : crée une nouvelle tache à répétition", anchor = "w")
    listBoxRepet = Listbox(fen, listvariable = listeDate)

    # Affichage
    lbTop.grid(row = 0, column = 0)
    listBoxRepet.grid(row = 1, column = 0)

    fen.activateandwait()
