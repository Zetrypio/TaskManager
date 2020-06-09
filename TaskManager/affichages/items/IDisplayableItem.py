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

    def __del__(self):
        """
        Le destructeur appel la méthode self#delete() si elle fonctionne.
        """
        try:
            self.delete()
        except:
            pass

    def redraw(self, frameOrCanvas):
        """
        Permet de mettre à jour l'affichage.
        @param frameOrCanvas: le Frame ou le Canvas sur lequel afficher cet objet.
        """
        raise NotImplementedError

    def updateColor(self):
        """
        Permet de mettre à jour la couleur de l'objet.
        """
        raise NotImplementedError
    
    def delete(self):
        """
        Permet de supprimer cet objet de l'affichage.
        Aussi appelée quand cet objet est supprimé.
        """
        raise NotImplementedError