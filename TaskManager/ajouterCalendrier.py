# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
from dialog import *










def ajouterHeure(heureMin, heureMax):
    nbHeure  = None
    position = None

    def onClose(bouton):
        # Permet de modifier les valeurs des variables
        nonlocal nbHeure, position
        if bouton == 'Ok':
            position = varRadioBouton.get()
            nbHeure = int(sb.get())

    # Pour adapter le nombre d'heure max du spinBoc
    def adapteSpinbox():
        if   varRadioBouton.get() == "Apres":
            sb.config(to = heureMax.total_seconds()//3600)
            # Si on dépasse, on reset au max
            if int(sb.get()) > heureMax.total_seconds()//3600:
                sb.set(int(heureMax.total_seconds()//3600))
        elif varRadioBouton.get() == "Avant":
            sb.config(to = heureMin.hour)

    fen = Dialog(title = "Nombre d'heure à ajouter",
           buttons = ("Ok", "Annuler"), command = onClose, exitButton = ('Ok', 'Annuler', "WM_DELETE_WINDOW"))
    # Binding des touches
    fen.bind_all("<Return>", lambda e: dialogue.execute("Ok"))
    fen.bind_all("<Escape>", lambda e: dialogue.execute("Annuler"))

    # Mettre les widgets
    frameHeure = Labelframe(fen, text="Combien d'heure ajouter ?")
    lb = Label(frameHeure,text="Nombre d'heure :")
    sb = Spinbox(frameHeure, from_ = 0, to = heureMax.total_seconds()//3600)
    sb.set(0)
    lb.pack(side=LEFT, fill=BOTH)
    sb.pack(side=LEFT, fill=X, expand=YES)



    framePos = Labelframe(fen, text="Où rajouter les heures ?")
    varRadioBouton = StringVar()
    r1 = Radiobutton(framePos, text = "Au début de la journée", variable = varRadioBouton, value = "Avant", command = adapteSpinbox)
    r2 = Radiobutton(framePos, text = "À la fin de la journée", variable = varRadioBouton, value = "Apres", command = adapteSpinbox)
    r1.grid(row=0, sticky="w")
    r2.grid(row=1, sticky="w")

    frameHeure.pack(side=TOP, expand=YES, fill=BOTH)
    framePos.pack(side=TOP, expand=YES, fill=BOTH)

    varRadioBouton.set("Apres")




    # Active et attend (un peu comme une mainloop)
    fen.activateandwait()
    return nbHeure, position

if __name__=='__main__':
    import Application
    Application.main()