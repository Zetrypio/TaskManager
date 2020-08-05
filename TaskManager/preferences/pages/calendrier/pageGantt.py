# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..AbstractPage import *

class PageGantt(AbstractPage):
    def __init__(self, master, **kwargs):
         # Note : self.master renvoie a ParametrageZone
         # Note : Si on rajoute une option, ne pas oublier d'ajouter la variable de contrôle à self._listData.append([variable, "texte explicatif", valeurParDefaut])
         # Note : Si l'option que l'on souhaite ajouter nécéssite un redémarrage pour s'appliquer, utiliser la méthode "self.__addDataNeedRestart(liste)", avec la même liste que pour self._listData

        super().__init__(master,nom = "Gantt", iid_parent ="-Calendrier", **kwargs)

    "" # Marque pour le repli de code
    ###################################
    # Méthodes liées à la fermeture : #
    ###################################
    ""
    def appliqueEffet(self, application):
        pass
        #self._makeDictAndSave() Quand il y aura des choses ici
