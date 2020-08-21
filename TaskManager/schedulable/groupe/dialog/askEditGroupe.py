# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.Dialog import *

from schedulable.groupe.dialog.GroupeParametre import *

def askEditGroupe(groupe):
    """
    Dialogue qui édite le groupe sur ses paramètres
    @param groupe : <Groupe> le groupe à modifier
    """
    def onClose(button):
        if button == "Ok":
            paramGroupe.onClose()
        elif button == "Supprimer":
            groupe.delete()
        fen.destroy()

    fen = Dialog(title = "Édition de \"%s\""%groupe.getNom(), buttons = ("Ok", "Supprimer",  "Annuler"), exitButton = ("Ok", "Supprimer",  "Annuler"), command = onClose)
    paramGroupe = GroupeParametre(fen, groupe)
    paramGroupe.pack(fill = BOTH, expand = YES)
    fen.activateandwait()

