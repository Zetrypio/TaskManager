# *-* coding:utf-8 *-*



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
        if self.__class__ == IDisplayableItem: raise RuntimeError("Can't instantiate interface IDisplayableItem directly.")

    "" # Marque pour que le repli de code fasse ce que je veux
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def delete(self):
        """
        Permet de supprimer cet objet de l'affichage.
        Aussi appelée quand cet objet est supprimé.
        """
        raise NotImplementedError

    def redraw(self, frameOrCanvas):
        """
        Permet de mettre à jour l'affichage.
        @param frameOrCanvas: le Frame ou le Canvas sur lequel afficher cet objet.
        """
        raise NotImplementedError

    def updateColor(self, frameOrCanvas):
        """
        Permet de mettre à jour la couleur de l'objet.
        """
        raise NotImplementedError(self.__class__.__name__)
