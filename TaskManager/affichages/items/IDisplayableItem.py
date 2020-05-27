# -*- coding:utf-8 -*-

# Interface
class IDisplayableItem:
    """
    Interface correspondant aux objets affichables dans
    les affichages comme calendrier classique ou gantt par exemple.
    """
    def __init__(self):
        """
        Constructeur interdisant l'instanciation direct de IDisplayableItem.
        """
        if self.__class__ == IDisplayableItem: raise RuntimeError("Can't instanciate interface IDisplayableItem directly.")
    
    def redraw(self, frameOrCanvas):
        """
        Permet de mettre à jour l'affichage.
        @param frameOrCanvas: le Frame ou le Canvas sur lequel afficher cet objet.
        """
        raise NotImplementedError
    
    def delete(self):
        """
        Permet de supprimer cet objet de l'affichage.
        """
        raise NotImplementedError