# -*- coding:utf-8 -*-
from .IDisplayableItem import *

# super classe abstraite
class AbstractMultiFrameItem(IDisplayableItem):
    """
    Classe représentant un item qui peut s'afficher dans
    un ou plusieurs cadre (Frame) de tkinter.
    """
    def __init__(self, master, schedulable):
        """
        Constructeur de l'item s'affichant dans plusieurs Frame() de tkinter.
        @param master: l'affichage de calendrier sur lequel vont s'afficher
        les différents cadres de cet objet. Il ne s'agit pas de l'argument passé
        dans le constructeur de ses cadre. Celui-ci sera à donner dans la méthode
        redraw() de cet objet.
        @param schedulable: l'objet à afficher parmi les différents cadre de cet objet.
        """
        if self.__class__ == AbstractMultiFrameItem: raise RuntimeError("Can't instanciate abtract class AbstractMultiFrameItem directly.")
        super().__init__()
        self.master = master
        self._listeCadre = []
        self._schedulable = schedulable

    def getRepartition(self):
        """
        Permet de savoir de où à où les différents cadre doivent aller.
        En effet, une tâche peut par exemple se dérouler sur plus d'un jour.
        Dans ce cas, la tâche est affichée 2 fois (ou plus si nécéssaire),
        1 fois par jours. Dès qu'il y a une découpe (nouveau jour, séparation
        pour un groupe etc.), cela va créer un nouveau cadre. Chaque éléments
        de la répartition est un ensemble datetime début et datetime fin pour
        indiquer de quand à quand ce cadre en question doit être fait.

        @return un générateur ou itérateur ou itérable (liste) pouvant être
        parcourru par une boucle for. Chaque élément doit être une paire de
        datetime indiquant le début et la fin de ce cadre.
        """
        return self._schedulable.getRepartition()
    
    def isPartVisible(self, part):
        """
        Permet de savoir si la partie est visible.
        @return True si la partie est visible.
        @return False si la partie n'est pas visible.
        """
        return self.master.isPartVisible(part)

#    def getPartsNumberAt(self, part):
#        """
#        Permet de savoir le nombre de parties qui sont en même temps,
#        à savoir le nombre de colonnes nécéssaire dans un affichage type
#        calendrier classique pour afficher toutes les tâches qui seraient
#        en même temps. Si il n'y a pas de tâches qui se superposent, cela
#        peut renvoyer plus que 1, mais dans ce cas le getColumnSpanAt renverra
#        le même nombre également.
#        @return le nombre de partitions en même temps en tant qu'int.
#        """
#        return self.master.getColumnsNumberAt(part)
    
    def getPartPosition(self, part):
        """
        Permet de savoir la position de la partition parmi les autres.
        @return la position de cette partition en tant qu'int répartie sur
        l'ensemble de celles qui sont en même temps.
        """
        return self.master.getColumnsPositionAt(part)
    
    def getPartSpan(self, part):
        """
        Permet de savoir sur combien se répartie la partition.
        """
        return self.master.getPartSpan(part)
