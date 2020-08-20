# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.Dialog import *

from schedulable.task.dialog.TaskParametre import *


def askEditTask(task):
    """
    Dialogue qui édite la tache sur ses paramètres
    @param task : <Task> la tache à modifier
    """
    def onClose(button):
        if button == "Ok":
            parametrage.onClose()
        elif button == "Supprimer":
            task.delete()
        fen.destroy()


    fen = Dialog(title = "Édition de \"%s\""%task.getNom(), buttons = ("Ok", "Supprimer", "Annuler"), exitButton = ("Ok", "Supprimer", "Annuler"), command = onClose) # Ajouter un supprimer
    parametrage = TaskParametre(fen, task)
    parametrage.pack(fill = BOTH, expand = YES)
    fen.activateandwait()
