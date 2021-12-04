# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from tkinter.messagebox import showerror

from util.widgets.Dialog import *

def askChangeProfil(profilManager):
    """
    Dialogue qui demande sur quel profil on veut changer.
    """
    PROFIL_ACTIF = profilManager.getListeProfilsUser()[0]

    # Callback :
    def onClose(button):
        PROFIL_SELECTED = cbProfil.get()

        if button == "Charger":
            profilManager.switchProfil(PROFIL_SELECTED or PROFIL_ACTIF)

        elif button == "Nouveau":
            if profilManager.createProfil(False):
                cbProfil.config(values = profilManager.getListeProfilsUser()[:])
                cbProfil.set(profilManager.getListeProfilsUser()[-1])

        elif button == "Supprimer":
            if PROFIL_ACTIF == PROFIL_SELECTED:
                showerror("Suppression impossible", "Impossible de supprimer le profil actif, Veuillez changer de profil pour effectuer la suppression.")

            elif askyesnowarning("Confirmation de suppression", "Voulez-vous vraiment supprimer ce profil ?\nSi vous êtes le seul utilisateur de ce profil, il sera détruit à tout jamais."):
                profilManager.deleteProfil(PROFIL_SELECTED)
                cbProfil.config(values = profilManager.getListeProfilsUser()[:])
                cbProfil.set(PROFIL_ACTIF)


    # Fenêtre du dialogue :
    fen = Dialog(
        title = "Changer de profil",
        buttons=("Charger", "Nouveau", "Supprimer", "Annuler"),
        command=onClose,
        exitButton=("Charger", "Annuler", "WM_DELETE_WINDOW")
    )

    # Widgets :
    Label(fen, text = "Profils :").pack(padx = (2, 0), pady = 2, side = LEFT)
    cbProfil = Combobox(fen, values = profilManager.getListeProfilsUser()[:], state = "readonly")
    cbProfil.set(cbProfil.cget("values")[0])
    cbProfil.pack(side = BOTTOM, fill = X, expand = YES, padx = 2, pady = 2)

    # Activation du dialogue :
    fen.activateandwait()
