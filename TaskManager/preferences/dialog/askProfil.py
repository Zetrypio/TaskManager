# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
import os


from util.widgets.Dialog import *
from .askFolder import *

def askProfil(obligatoire, app):
    """
    Dialogue qui demande a créer un profil
    @param obligatoire : <bool> True  = création d'un profil, pour un user si il en a 0
                                False = création d'un profil, facultatif
    @param app         : <Application> pour quitter en cas de Bool True et croix
    """
    nom    = None
    folder = None

    def onClose(bouton):
        # Permet de modifier les valeurs des variables
        nonlocal nom, folder
        if bouton == 'Ok':
            # récup les valeurs
            nom = entryNom.get()
            folder = varEntryPath.get()
        elif obligatoire:
            if not askyesnowarning(title = "Erreur", message="Vous n'avez pas encore de profil, vous devez un créer un pour commencer.\nCliquez sur \"non\" pour fermer l'application"):
                # Si vraiment il est concient et qu'il veut quitter...
                app.after(10,quit())

            return
        fen.destroy()

    def parcourir():
       """
       fonction qui demande où stocker les fichier ET vérifie si le dossier est bien vide
       """
       path = askFolder(vide = True)
       # on set le nouveau path
       if path is not None:
           varEntryPath.set(path)


    fen = Dialog(title = "Nombre d'heure à déplacer",
           buttons = ("Ok", "Annuler"), command = onClose, exitButton = ('Ok', 'Annuler', "WM_DELETE_WINDOW"))
    # Binding des touches
    fen.bind_all("<Return>", lambda e: fen.execute("Ok"))
    fen.bind_all("<Escape>", lambda e: fen.execute("Annuler"))

    # Widgets
    lbDebut  = Label(fen, text = "Créez un profil pour sauvegarder vos données")
    lbNom    = Label(fen, text = "Nom :")
    entryNom = Entry(fen)

    framePath = Frame(fen)
    lbPathCustomFile = Label(framePath, text = "Chemin d'enregistrement de vos fichiers de préférences")
    varEntryPath = StringVar()
    entryPathCustomFile = Entry(framePath, state="normal", textvariable = varEntryPath)
    btnParcourir = Button(framePath, text = "...", command = parcourir, width=3)

    # Affichage
    lbDebut.grid(column = 0, row = 0, sticky="wens")
    lbNom.grid(column = 0, row = 1, sticky = "w")
    entryNom.grid(column = 1, row = 1, sticky = "we")
    framePath.grid(column = 0, row = 2, columnspan = 2, sticky = "wens")
    lbPathCustomFile.grid(column = 0, row = 0, sticky = "w")
    entryPathCustomFile.grid(column = 0, row = 1, sticky = "we")
    btnParcourir.grid(column = 1, row = 1, sticky = "w")

    # preset
    entryNom.insert(END, os.getlogin())
    varEntryPath.set(os.path.expanduser("~/.taskManager/"))


    fen.activateandwait()
    return nom, folder
