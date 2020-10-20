# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.Dialog import *
from util.util import adaptDate

def askSeparateRepetitiveTask(task):
    """
    Dialogue qui gère les taches à répétitions (les jours à ne pas afficher et autres
    @param task : <Task> tache dont on gère les répétition
    """
    def onClose(button):
        if button == "Ok":
            print("ok.")

    def scinder():
        """
        Fonction qui scinde la répétition en une nouvelle répétition à partir
        de la répétition selectionné
        """
        selected = listBoxRepet.curselection()

    def separate():
        """
        Fonction qui ajoute une répétition à ne pas faire
        + crée une autre tache à la date ou la précédante est annulé
        """
        selected = listBoxRepet.curselection()

    # Variable
    listeDate = StringVar()

    # Affctation
    listeDate.set([adaptDate(task.getData(), (numero*task.getRep() + task.getDebut()).date()) + " - " + str((numero*task.getRep() + task.getDebut()).time()) for numero in range(task.getNbRep())]) # En gros "date joli - time"


    fen = Dialog(title = "Répétition de \"%s\""%task.getNom(), buttons = ("Ok", "Annuler"), exitButton = ("Ok", "Annuler", "WM_DELETE_WINDOW"), command = onClose)

    # Liste de widget
    lbTop = Label(fen, text = "Gestion des répétitions :\n\t- (*)Dissocier : retire une tache des répétition\n\t- Scinder : crée une nouvelle tache à répétition", justify = LEFT)
    listBoxRepet = Listbox(fen, listvariable = listeDate, selectmode = "single")
    frameBtn = Frame(fen)
    btnSeparate = Button(frameBtn, text = "Dissocier", command = separate)
    btnScinder = Button(frameBtn, text = "Scinder", command = scinder)

    # Affichage
    lbTop.grid(row = 0, column = 0, columnspan = 2)
    listBoxRepet.grid(row = 1, column = 0, sticky = "we", padx = 3)
    frameBtn.grid(row = 1, column = 1, sticky = "nsew")
    btnSeparate.grid(row = 0, column = 0, sticky = "we")
    btnScinder.grid(row = 1, column = 0, sticky = "we")

    fen.activateandwait()
