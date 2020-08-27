# -*- coding:utf-8 -*-

class ITaskEditorDisplayableObject:
    """
    Cette interface liste les méthode qu'il est nécessaire
    d'implémenter pour les objets s'affichant dans le
    Treeview du TaskEditor. (Qui en vrai gère plus que de
    simple tâches - groupes ou périodes sont les exemples).
    Ces méthodes permettent de choisir ce qui est affiché
    dans ce Treeview, ainsi que le menu quand on fait
    clic-droit dessus.
    """
    def __init__(self):
        if self.__class__ == TaskEditorDisplayableObject:
            raise RuntimeError("Impossible d'instancier l'interface ITaskEditorDisplayableObject directement")

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def getColor(self):
        """
        Getter pour la couleur de l'objet à mettre dans le treeview.
        @return la couleur de l'objet à mettre dans le treeview.
        """
        raise NotImplementedError

    def getFilterStateWith(self, filter):
        """
        @return  1 Si l'objet est acceptée par le filtre et qu'elle doit être prioritaire.
        @return  0 Si l'objet est acceptée par le filtre sans être prioritaire.
        @return -1 Si l'objet n'est pas accepté par le filtre.
        """
        raise NotImplementedError

    def getHeader(self):
        """
        @return un couple <nom, valeur> qui seront utilisés
        pour la ligne d'entête de l'affichage de cette objet dans l'arbre.
        """
        raise NotImplementedError

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def iterateDisplayContent(self):
        """
        @return l'un parmi itérateur, itérable (listes etc.) ou générateur
        dont chaque éléments est soit:
         - une paire de str, pour l'affichage d'un ligne. Les 2 textes
           correspondent respectivement à la première et la deuxième colonne.
         - un dictionnaire, permettant de configurer les arguments
           donnés à la prochaine sous-itération récursive.
         - un ITaskEditorDisplayableObjec, pour la récursion.
           sa méthode iterateDisplayContent sera appelée aussi,
           avec les paramètres données dans le dernier yield d'un
           dictionnaire (voir juste au-dessus).
        
        Il est possible d'utiliser la même configuration pour plusieurs
        ITaskEditorDisplayableObject, il suffit de le yield une seule fois
        avant les yields des ITaskEditorDisplayableObject.
        Cependant, si vous voulez changer la configuration, il suffit de
        yield un autre dictionnaire de configuration.

        Utiliser "yield from" si vous faites un générateur
        pour faire cette récursion vous permettra
        d'ajouter pleins de ITaskEditorDisplayableObject,
        d'un coup, en tant que sous branche de la dernière créée.
        Il est aussi possible de yield from autre chose qu'une liste/
        itérateur/itérable/générateur de ITaskEditorDisplayableObject,
        mais à condition que ce soit l'un (ou plusieurs) des types
        énoncés ci-dessus.
        """
        raise NotImplementedError

    def setRMenuContent(self, taskEditor, rmenu):
        """
        Permet de rajouter les commandes au RMenu() de cet objet si il est présent.
        Si cet objet n'a pas besoin de RMenu() dans le TaskEditor(), il faut simplement
        que cette méthode retourne False
        @param taskEditor : permet de faire des interactions avec le TaskEditor().
        @param rmenu : le RMenu() sur lequel rajouter les commandes et tout et tout.
        @return True si le RMenu() existe, False sinon.
        """
        raise NotImplementedError

    def selectInTaskEditor(self):
        """
        Méthode qui demande au TaskEditor de sélectionner la ligne qui correspond au schedulable
        """
        raise NotImplementedError
