# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from affichages.periode.Periode import *
from util.widgets.Dialog import *

def askDecalJour(debut, fin, totBloque, tarBloque):
    """
    Dialog pour demander comment décaler les tâches
    @param debut     : (date) jour de début de la période
    @param fin       : (date) jour de fin de la période
    @param totBloque : (int) nombre de jours à partir duquel le blocage devient utile
    @param tarBloque : (int) nombre de jours à partir duquel le blocage devient utile
    """
    nbJour  = None
    position = None
    param    = None

    def onClose(bouton):
        # Permet de modifier les valeurs des variables
        nonlocal nbJour, position, param
        if bouton == 'Ok':
            position = varRadioGestion.get()
            param = varRadioParam.get()
            nbJour = int(sb.get())
            if varRadioGestion.get() == "tot":
                nbJour = nbJour*-1
        fen.destroy()

    # Pour adapter le nombre d'jour max du spinBoc
    def adapteSpinbox():
        newVar = 0
        if   varRadioGestion.get() == "tot" and varRadioParam.get() == "bloquer":
            newVar = totBloque
        elif varRadioGestion.get() == "tard" and varRadioParam.get() == "bloquer":
            newVar = tarBloque
        elif varRadioGestion.get() == "tot" or varRadioGestion.get() == "tard":
            newVar = "+inf"

        # On config
        sb.config(to = newVar)
        # Si on dépasse, on reset au max
        if isinstance(newVar, str):
            return
        if int(sb.get()) > newVar:
            sb.set(int(newVar))

    fen = Dialog(title = "Nombre de jours à déplacer",
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

    frameJour = Labelframe(fen, text="Déplacer de combien de jours ?")
    lb = Label(frameJour,text="Nombre de jours :")
    sb = Spinbox(frameJour, from_ = 0, to = "+inf")
    sb.set(0)
    lb.pack(side=LEFT, fill=BOTH)
    sb.pack(side=LEFT, fill=X, expand=YES)

    frameParametre = Frame(fen)
    varRadioParam = StringVar()
    rP1 = Radiobutton(frameParametre, text = "Garder la même durée entre chaque tache", variable = varRadioParam, value = "duree", command = adapteSpinbox)
    rP2 = Radiobutton(frameParametre, text = "Garder les tâches entre le %02i/%02i et le %02i/%02i"%(debut.day, debut.month, fin.day, fin.month), variable =varRadioParam, value = "bloquer", command = adapteSpinbox)
    rP1.grid(row=0, sticky="w")
    rP2.grid(row=1, sticky="w")

    framePos.pack(    side = TOP, expand = YES, fill = BOTH)
    frameJour.pack(  side = TOP, expand = YES, fill = BOTH)
    frameParametre.pack(  side = TOP, expand = YES, fill = BOTH)

    varRadioGestion.set("tard")
    varRadioParam.set("duree")

    # Active et attend (un peu comme une mainloop)
    fen.activateandwait()
    return nbJour, position, param

def askComplicationjour(tache, periodeManager):
    choix   = None
    periode = None

    def onClose(bouton):
        # Permet de modifier les valeurs des variables
        nonlocal choix, periode
        if bouton == 'Ok':
            choix = varRadio.get()
            if choix == "changer":
                for p in periodeManager.getPeriodes():
                    if p.nom == combo.get():
                        periode = p
        fen.destroy()

    def stateCombobox():
        if varRadio.get() == "changer":
            combo.config(state=ACTIVE)
        else:
            combo.config(state=DISABLED)
    fen = Dialog(title = "%s n'est pas dans la période active"%tache.getNom(),
        buttons = ("Ok", "Annuler"), command = onClose, exitButton = ('Ok', 'Annuler', "WM_DELETE_WINDOW"))

    # Binding des touches
    fen.bind_all("<Return>", lambda e: fen.execute("Ok"))
    fen.bind_all("<Escape>", lambda e: fen.execute("Annuler"))

    l = Label(fen, text="La tache \"%s\" se trouve maintenant hors de la période. Que voulez-vous faire ?"%tache.getNom())

    frameRadio = LabelFrame(fen, text="Options")
    varRadio = StringVar()
    r1 = Radiobutton(frameRadio, text="Agrandir la période", value = "agrandir", variable = varRadio, command = stateCombobox)
    r2 = Radiobutton(frameRadio, text="Faire de %s une tache indépendante"%tache.getNom(), value = "independante", variable = varRadio, command = stateCombobox)
    r3 = Radiobutton(frameRadio, text="Supprimer %s."%tache.getNom(), value = "supprimer", variable = varRadio, command = stateCombobox)
    r4 = Radiobutton(frameRadio, text="Changer la période de %s."%tache.getNom(), value = "changer", variable = varRadio, command = stateCombobox)
    # valeur par défaut :
    varRadio.set("agrandir")

    r1.grid(sticky="w")
    r2.grid(row=1, sticky="w")
    r3.grid(row=2, sticky="w")
    r4.grid(row=3, sticky="w")

    periodesExistantes = periodeManager.getPeriodes()
    pp = Periode(periodeManager, "", tache.getDebut().date(), tache.getFin().date(), "")
    periodesExistantes = [p.nom for p in periodesExistantes if p.intersectWith(pp)]
    combo = Combobox(frameRadio, values = periodesExistantes)

    combo.grid(row=3,column=1, sticky="we")
    if periodesExistantes:
        combo.set(combo.cget("values")[0])
    else:
        combo.config(state=DISABLED)
        r4.config(state=DISABLED)

    l.pack()
    frameRadio.pack(expand=YES, fill=BOTH, pady=4, padx=4)




    # Active et attend (un peu comme une mainloop)
    fen.activateandwait()
    return choix, periode


