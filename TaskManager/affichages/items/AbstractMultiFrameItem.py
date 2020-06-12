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
        if self.__class__ == AbstractMultiFrameItem: raise RuntimeError("Can't instantiate abstract class AbstractMultiFrameItem directly.")
        super().__init__()
        self.master = master
        self._schedulable = schedulable

    def getSchedulable(self):
        return self._schedulable

    def getRepartition(self):
        """
        Permet de savoir de où à où les différents cadre doivent aller.
        En effet, une tâche peut par exemple se dérouler sur plus d'un jour.
        Dans ce cas, la tâche est affichée 2 fois (ou plus si nécessaire),
        1 fois par jours. Dès qu'il y a une découpe (nouveau jour, séparation
        pour un groupe etc.), cela va créer un nouveau cadre. Chaque éléments
        de la répartition est un DatetimeItemPart pour indiquer de quand
        à quand ce cadre en question doit être fait.

        @return un générateur ou itérateur ou itérable (liste) pouvant être
        parcouru par une boucle for. Chaque élément doit être une paire de
        datetime.datetime() indiquant le début et la fin de ce cadre.
        """
        return self._schedulable.getRepartition(self.master)

    
    def getFirstPart(self):
        """
        Getter pour obtenir la première part affichée de #getRepartition(displayedCalendar).
        @return la première datetimeItemPart affichée parmi toutes.
        """
        return self._schedulable.getFirstPart(self.master)

    def getLastPart(self):
        """
        Getter pour obtenir la dernière part affichée de #getRepartition(displayedCalendar).
        @return la dernière datetimeItemPart affichée parmi toutes.
        """
        return self._schedulable.getLastPart(self.master)

    def getVisiblePart(self, part):
        """
        Permet d'obtenir la partie visible d'un DatetimeItemPart.
        @return l'objet inchangé si celui-ci est complètement visible.
        @return un nouveau DatetimeItemPart si celui-ci est partiellement visible,
        ce nouvel objet sera normalement entièrement visible.
        @return None si l'objet n'est pas visible du tout.
        """
        return self.master.getVisiblePart(part)
    
    def getPartPosition(self, part):
        """
        Permet de savoir la position d'un DatetimeItemPart parmi les autres.
        @return la position de ce DatetimeItemPart en tant qu'int répartie sur
        l'ensemble de ceux qui sont en même temps.
        """
        return self.master.getPartPosition(part)
    
    def getPartSpan(self, part):
        """
        Permet de savoir sur combien se répartie le DatetimeItemPart.
        @return le nombre de sur combien se répartie le DatetimeItemPart.
        """
        return self.master.getPartSpan(part)


