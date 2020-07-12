# *-* coding:utf-8 *-*
from tkinter.messagebox import showerror
from tkinter.filedialog import askdirectory
from os import listdir

def askFolder(vide = False):
   """
   fonction qui demande un dossier
   @param vide  : <bool> Si le dossier doit être vide
   @return path : <str>  Indique le chemin du dossier
   """
   path = askdirectory()
   if not path:
       return None

   if vide:
       if testVide(path) is None:
           return None

   return path

def testVide(path):
    """
    Fonction qui regarde si c'est vide
    @param path : <str> chemin du dossier
    """
    # condition "if not" car il détecte desktop.ini parfois ...
    while len([i for i in listdir(path) if not i == "desktop.ini"])!=0:
        showerror(title="Chemin invalide", message="Le dossier que vous avez choisi n'est pas valide.\nLe dossier de destination doit être vide.")
        path = askdirectory()
        # si on clique sur la croix/cancel
        if not path:
            return None
