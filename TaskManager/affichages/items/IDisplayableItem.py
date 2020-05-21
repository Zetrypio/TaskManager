# -*- coding:utf-8 -*-

# Interface
class IDisplayableItem:
    """
    Interface correspondant aux objets affichables dans
    les affichages comme calendrier classique ou gantt par exemple.
    """
    def __init__(self):
        if self.__class__ == AbstractMultiFrameItem: raise RuntimeError("Can't instanciate interface IDisplayableItem directly.")
    
    def redraw(self):
        """Permet de mettre à jour l'affichage."""
        raise NotImplementedError