# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from tkinter.messagebox import showerror
import datetime

from util.widgets.Dialog import *
def askDureeTache(master, longueurPeriode):
    """
    Permet de demander la durée de la tâche à l'utilisateur.
    @param longueurPeriode = longueur de la periode
    @return la durée choisie par l'utilisateur.
    """
    # Fonction quand on ferme le dialogue :
    duree = None
    def onClose(bouton):
        """Exécutée quand l'un des boutons du dialogue est pressé."""
        nonlocal duree
        if bouton == "Ok":
            duree = datetime.timedelta(days = int(d.get()), hours = int(h.get()), minutes = int(m.get()))
            if duree > datetime.timedelta():
                fen.quit()
                fen.destroy()
            else:
                showerror("Durée invalide", "Veuillez mettre une durée plus grande que 0.")
        else:
            fen.destroy()
    def adapteHeureJour():
        """Adaptation des heures et des jours quand on augmente ou diminue trop les heures ou les minutes."""
        minutes = int(m.get())
        heures  = int(h.get())
        jours   = int(d.get())

        while minutes >= 60:
            minutes -= 60
            heures += 1
        while minutes < 0:
            minutes += 60
            heures -= 1
        while heures >= 24:
            heures -= 24
            jours += 1
        while heures < 0:
            heures += 24
            jours -= 1
        jours = max(0, min(jours, longueurPeriode.days))

        m.set(minutes)
        h.set(heures)
        d.set(jours)

    # Création du dialogue :
    fen = Dialog(master, title = "Choix de la durée de la tâche",
               buttons = ("Ok", "Annuler"), command = onClose, exitButton = ('Annuler',))
    # Widgets du dialogue :
    Label(fen, text = "Choisissez la durée de la Tâche").pack(side = TOP, fill = X)
    d = Spinbox(fen, from_ = 0, to = longueurPeriode.days, increment = 1, width = 4)
    d.pack(side = LEFT)
    Label(fen, text = "Jours").pack(side = LEFT)
    h = Spinbox(fen, from_ = -1, to = 24, increment = 1, width = 4, command = adapteHeureJour)
    h.pack(side = LEFT)
    Label(fen, text = "Heures").pack(side = LEFT)
    m = Spinbox(fen, from_ = -1, to = 60, increment = 1, width = 4, command = adapteHeureJour)
    m.pack(side = LEFT)
    Label(fen, text = "Minutes").pack(side = LEFT)
    d.set(0)
    h.set(1)
    m.set(0)
    # lancement du dialogue:
    fen.activateandwait()
    return duree
