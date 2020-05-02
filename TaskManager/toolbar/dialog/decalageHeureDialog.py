# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.widgets.Dialog import *

def askDecalHeure(heureRetirerMax, heureAjoutMax):
    nbHeure = None
    position = None

    def onClose(bouton):
        # Permet de modifier les valeurs des variables
        nonlocal nbHeure, position
        if bouton == 'Ok':
            position = varRadioGestion.get()
            nbHeure = int(sb.get())
            if varRadioGestion.get() == "tot":
                nbHeure = nbHeure*-1
        fen.destroy()

    # Pour adapter le nombre d'heure max du spinBoc
    def adapteSpinbox():
        newVar = 0
        if   varRadioGestion.get() == "tot":
            newVar = heureRetirerMax
        elif varRadioGestion.get() == "tard":
            newVar = heureAjoutMax

        # On config
        sb.config(to = newVar)
        # Si on dépasse, on reset au max
        if int(sb.get()) > newVar:
            sb.set(int(newVar))

    fen = Dialog(title = "Nombre d'heure à déplacer",
           buttons = ("Ok", "Annuler"), command = onClose, exitButton = ('Ok', 'Annuler', "WM_DELETE_WINDOW"))
    # Binding des touches
    fen.bind_all("<Return>", lambda e: fen.execute("Ok"))
    fen.bind_all("<Escape>", lambda e: fen.execute("Annuler"))

    # Mettre les widgets
    framePos = Frame(fen)
    varRadioGestion = StringVar()
    rG1= Radiobutton(framePos, text = "Déplacer plus tot", variable = varRadioGestion, value = "tot", command = adapteSpinbox)
    rG2= Radiobutton(framePos, text = "Déplacer plus tard", variable = varRadioGestion, value = "tard", command = adapteSpinbox)
    rG1.grid(row=0, sticky="w")
    rG2.grid(row=1, sticky="w")

    frameHeure = Labelframe(fen, text="Déplacer de combien d'heure ?")
    lb = Label(frameHeure,text="Nombre d'heure :")
    sb = Spinbox(frameHeure, from_ = 0, to = heureAjoutMax)
    sb.set(0)
    lb.pack(side=LEFT, fill=BOTH)
    sb.pack(side=LEFT, fill=X, expand=YES)

    framePos.pack(    side = TOP, expand = YES, fill = BOTH)
    frameHeure.pack(  side = TOP, expand = YES, fill = BOTH)
    Label(fen, text="Toutes les taches vont être décalées.\nSi c'est un nombre d'heures trop important, elles seront placées au début ou en fin de journée.").pack(side = TOP, expand = YES, fill = X)

    varRadioGestion.set("tard")



    # Active et attend (un peu comme une mainloop)
    fen.activateandwait()
    return nbHeure, position
