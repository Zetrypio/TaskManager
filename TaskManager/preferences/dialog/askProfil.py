# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
import os


from util.widgets.Dialog import *
from .askFolder import *

def askProfil(obligatoire, app, listeProfil):
    """
    Dialogue qui demande a créer un profil
    @param obligatoire : <bool> True  = création d'un profil, pour un user si il en a 0
                                False = création d'un profil, facultatif
    @param app         : <Application> pour quitter en cas de Bool True et croix
    @param listeProfil : <dict> de tout les profils avec leurs paths, on dois la passer car la premiere fois on peut pas passer par l'app car le profil manager n'est pas encore crée
    """
    listeFolder = listeProfil.values() # <dict_values> contient tous les paths des profils
    nom    = None
    folder = None

    def onClose(bouton):
        # Permet de modifier les valeurs des variables
        nonlocal nom, folder
        # Récupération des valeurs
        nom = entryNom.get()
        folder = varEntryPath.get()

        if bouton == "Ok" :
            # On regarde si le dossier est vide
            testVide(folder)
            # Ne cherche que dans les "keys" qui sont les noms des profils ☺
            if nom in listeProfil:
                showerror(title="Erreur", message="Ce nom est déjà pris pour un autre profil")
                return
            elif folder in listeFolder:
                showerror(title="Erreur", message="Ce dossier est déjà pris pour un autre profil")
                return

        # Dans tous les cas quand c'est annulé :
        else:
            if obligatoire:
                if not askyesnowarning(title = "Erreur", message="Vous n'avez pas encore de profil, vous devez un créer un pour commencer.\nCliquez sur \"non\" pour fermer l'application"):
                    # Si vraiment il est conscient et qu'il veut quitter...
                    app.destroy()
                    raise SystemExit(0) # Pour finir le programme sans soucis
                return
            else:
                nom = folder = None

        fen.destroy()

    def parcourir():
       """
       fonction qui demande où stocker les fichier ET vérifie si le dossier est bien vide
       """
       path = askFolder(vide = True)
       # on set le nouveau path
       if path is not None:
           varEntryPath.set(path)


    fen = Dialog(master = app, title = "Création d'un profil",
           buttons = ("Ok", "Annuler"), command = onClose, exitButton = [])
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
    lbDebut.grid(column = 0, row = 0, columnspan = 2, sticky="wens", pady=3)
    lbNom.grid(column = 0, row = 1, sticky = "w")
    entryNom.grid(column = 1, row = 1, sticky = "we")
    framePath.grid(column = 0, row = 2, columnspan = 2, sticky = "wens")
    lbPathCustomFile.grid(column = 0, row = 0, sticky = "w")
    entryPathCustomFile.grid(column = 0, row = 1, sticky = "we")
    btnParcourir.grid(column = 1, row = 1, sticky = "w")

    # preset
    entryNom.insert(END, os.getlogin())
    varEntryPath.set((os.path.expanduser("~/.taskManager/")).replace("/", os.sep).replace("\\", os.sep))


    fen.activateandwait()
    return nom, folder
