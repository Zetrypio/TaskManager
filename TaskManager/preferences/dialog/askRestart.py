# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from util.widgets.Dialog import *

def askRestart():
    """
    Dialog qui demande si l'utilisateur veut redemarrer l'application
    """
    restart = None
    def Onclose(button):
        nonlocal restart
        if button == "Redémarrer":
            restart = True
        elif button == "Redémarrer plus tard" or button == 'WM_DELETE_WINDOW':
            restart = False
        else :
            restart = False

    f = Dialog(master = None, title = "Redémarrage requis", buttons = ("Redémarrer", "Redémarrer plus tard"), defaultbutton = "Redémarrer", exitButton = ("Redémarrer", "Redémarrer plus tard", 'WM_DELETE_WINDOW'), command = Onclose)

    l = Label(f, text = "Une ou plusieurs de vos modifications nécéssitent un redémarrage\nde l'applicationpour être correctement appliquées.\n\nVoulez-vous redémarrer l'application maintenant ?")
    l.pack()

    f.activateandwait()
    return restart
