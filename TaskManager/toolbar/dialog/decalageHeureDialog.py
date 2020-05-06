# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.widgets.Dialog import *

def askDecalHeure(heureRetirerMax, heureAjoutMax, debut, fin, totBloque, tarBloque):
    """
    Dialog pour demander comment décaler les taches
    @param heureRetirerMax : (int) nombre d'heure que l'on peut retirer maximum à la tache qui commence le plus tardivement
    @param heureAjoutMax   : (int) nombre d'heure que l'on peut ajouter maximum à la tache qui termine le plus tot
    @param debut           : (time) heure de début d'affichage
    @param fin             : (time) heure de fin d'affichage
    @param totBloque       : (int) nombre d'heure à partir duquelle le blocage devient utile
    @param tarBloque       : (int) nombre d'heure à partir duquelle le blocage devient utile
    """
    nbHeure  = None
    position = None
    param    = None

    def onClose(bouton):
        # Permet de modifier les valeurs des variables
        nonlocal nbHeure, position, param
        if bouton == 'Ok':
            position = varRadioGestion.get()
            param = varRadioParam.get()
            nbHeure = int(sb.get())
            if varRadioGestion.get() == "tot":
                nbHeure = nbHeure*-1
        fen.destroy()

    # Pour adapter le nombre d'heure max du spinBoc
    def adapteSpinbox():
        newVar = 0
        if   varRadioGestion.get() == "tot" and varRadioParam.get() == "bloquer":
            newVar = totBloque
        elif varRadioGestion.get() == "tot":
            newVar = heureRetirerMax
        elif varRadioGestion.get() == "tard" and varRadioParam.get() == "bloquer":
            newVar = tarBloque
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

    frameParametre = Frame(fen)
    varRadioParam = StringVar()
    rP1 = Radiobutton(frameParametre, text = "Garder la même durée entre chaque tache", variable = varRadioParam, value = "duree", command = adapteSpinbox)
    rP2 = Radiobutton(frameParametre, text = "Garder les taches entre %s h %s et %s h %s"%(debut.hour, debut.minute, fin.hour, fin.minute), variable =varRadioParam, value = "bloquer", command = adapteSpinbox)
    rP1.grid(row=0, sticky="w")
    rP2.grid(row=1, sticky="w")

    framePos.pack(    side = TOP, expand = YES, fill = BOTH)
    frameHeure.pack(  side = TOP, expand = YES, fill = BOTH)
    frameParametre.pack(  side = TOP, expand = YES, fill = BOTH)



    varRadioGestion.set("tard")
    varRadioParam.set("duree")



    # Active et attend (un peu comme une mainloop)
    fen.activateandwait()
    return nbHeure, position, param

def askChangerHeure():
    if askyesnowarning("Plage horaire trop court", "Une ou plusieurs taches ne sont plus visibles.\nVoulez-vous adapter la plage horaire ?"):
        return True
    else:
        return False
