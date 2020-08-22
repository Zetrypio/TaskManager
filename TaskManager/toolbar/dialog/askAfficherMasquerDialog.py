# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.Dialog import *

from .AfficherMasquerClass import *

def askAfficherMasquer(periodManager):
    """
    Dialogue qui permet de gérer la visibilitée des schedulables
    @param periodManager : <PeriodManager> celui de l'app
    @return masquage : <bool> True si au moins une tache n'est pas visible
    """
    masquage = False
    def onClose(b):
        nonlocal masquage
        if b == "Ok":
            gestion.onClose(b)
        if any(not t.isVisible() for t in periodManager.getActivePeriode().getPrimitivesSchedulables()):
            masquage = True
        else:
            masquage = False
        fen.destroy()

    fen = Dialog(title = "Afficher ou masquer des taches", buttons = ("Ok", "Annuler"), command = onClose)
    gestion = AfficherMasquer(fen, periodManager)
    gestion.pack(fill = BOTH, expand = YES)

    fen.activateandwait()
    return masquage

