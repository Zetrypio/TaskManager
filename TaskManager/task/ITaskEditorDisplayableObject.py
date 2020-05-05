# -*- coding:utf-8 -*-

class ITaskEditorDisplayableObject:
    def __init__(self):
        if self.__class__ == TaskEditorDisplayableObject:
            raise RuntimeError("Impossible d'instancier l'interface ITaskEditorDisplayableObject directement")
    def getHeader(self):
        """
        Retourne un couple <nom, valeur> qui seront utilisés
        pour la ligne d'entête de l'affichage de cette objet dans l'arbre.
        """
        raise NotImplementedError
    def iterateDisplayContent(self):
        """
        Retourne l'un parmi itérateur, itérable (listes etc.) ou générateur
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

        Utiliser "yield from" si vous faîtes un générateur
        pour faire cette récursion vous permettra
        d'ajouter pleins de ITaskEditorDisplayableObject,
        d'un coup, en tant que sous branche de la dernière créée.
        Il est aussi possible de yield from autre chose qu'une liste/
        itérateur/itérable/générateur de ITaskEditorDisplayableObject,
        mais à condition que ce soit l'un (ou plusieurs) des types
        énoncés ci-dessus.
        """
        raise NotImplementedError
    def getFilterStateWith(self, filter):
        """
        @return  1 Si l'objet est acceptée par le filtre et qu'elle doit être prioritaire.
        @return  0 Si l'objet est acceptée par le filtre sans être prioritaire.
        @return -1 Si l'objet n'est pas accetpée par le filtre.
        """
        raise NotImplementedError
    def getColor(self):
        """
        Getter pour la couleur de l'objet à mettre dans le treeview.
        """
        raise NotImplementedError