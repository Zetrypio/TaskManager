# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.widgets.Dialog import *
from util.importPIL import *

def askAjouterJour(totalJour):
    nbJour   = None
    position = None

    def onClose(bouton):
        # Permet de modifier les valeurs des variables
        nonlocal nbJour, position
        if bouton == 'Ok':
            position = varRadioBouton.get()
            nbJour = int(sb.get())
            if varRadioGestion.get() == "Retirer":
                nbJour = nbJour*-1
        fen.destroy()

    # Pour adapter le nombre de jour max du spinBox
    def adapteSpinbox():
        newVar = 0
        if   varRadioGestion.get() == "Retirer":
            newVar = totalJour
            # Si on dépasse, on reset au max
            if int(sb.get()) > newVar:
                sb.set(int(newVar))
        elif varRadioGestion.get() == "Ajouter":
            newVar = "+inf"
        # On config
        sb.config(to = newVar)

    fen = Dialog(title = "Nombre de jours à ajouter",
           buttons = ("Ok", "Annuler"), command = onClose, exitButton = ('Ok', 'Annuler', "WM_DELETE_WINDOW"))
    # Binding des touches
    fen.bind_all("<Return>", lambda e: fen.execute("Ok"))
    fen.bind_all("<Escape>", lambda e: fen.execute("Annuler"))

    # Mettre les widgets
    frameGestion = Frame(fen)
    varRadioGestion = StringVar()
    rG1= Radiobutton(frameGestion, text = "Ajouter les jours", variable = varRadioGestion, value = "Ajouter", command = adapteSpinbox)
    rG2= Radiobutton(frameGestion, text = "Retirer les jours", variable = varRadioGestion, value = "Retirer", command = adapteSpinbox)
    rG1.grid(row=0, sticky="w")
    rG2.grid(row=1, sticky="w")

    framejour = Labelframe(fen, text="Combien de jours ajouter ?")
    lb = Label(framejour,text="Nombre d'jour :")
    sb = Spinbox(framejour, from_ = 0, to="+inf")
    sb.set(0)
    lb.pack(side=LEFT, fill=BOTH)
    sb.pack(side=LEFT, fill=X, expand=YES)

    framePos = Labelframe(fen, text="Où rajouter les jours ?")
    varRadioBouton = StringVar()
    r1 = Radiobutton(framePos, text = "Au début de la période", variable = varRadioBouton, value = "Avant", command = adapteSpinbox)
    r2 = Radiobutton(framePos, text = "À la fin de la période", variable = varRadioBouton, value = "Apres", command = adapteSpinbox)
    r1.grid(row=0, sticky="w")
    r2.grid(row=1, sticky="w")

    frameGestion.pack(side = TOP, expand = YES, fill = BOTH)
    framejour.pack(  side = TOP, expand = YES, fill = BOTH)
    framePos.pack(    side = TOP, expand = YES, fill = BOTH)

    varRadioGestion.set("Ajouter")
    varRadioBouton.set("Apres")




    # Active et attend (un peu comme une mainloop)
    fen.activateandwait()
    return nbJour, position
