# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from util.widgets.Dialog import *

def askResetBind():
    """
    Dialogue qui demande quelle binding retrouver
    @return binding : <str> "defaut" -> cherche le binding par défaut
                            "custom" -> cherche l'ancien binding de l'utilisateur
                            "vide"   -> retire le binding ""
                      <None> -> annule l'opération
    """
    binding = None

    def onClose(btn):
        nonlocal binding
        if btn == "Annuler":
            pass
        elif btn == "Par défaut":
            binding = "defaut"
        elif btn == "Précédent":
            binding = "custom"
        elif btn == "Vide":
            binding = "vide"

        fen.destroy()

    fen = Dialog(title = "Choix du raccourci",  buttons=("Précédent", "Par défaut", "Vide", "Annuler"), command=onClose, exitButton = ("Précédent", "Par défaut", "Vide", "Annuler"))
    Label(fen, text = "Quelle est le raccourci que vous voulez retrouver ?").pack(expand = YES, fill = BOTH, padx=2, pady=2)

    fen.activateandwait()
    return binding
