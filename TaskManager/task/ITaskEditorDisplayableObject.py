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
        dont chaque éléments est soit une paire de str,
        ou un ensemble <ITaskEditorDisplayableObject, **kwargs>,
        pour la récursion.

        Utiliser "yield from" si vous faîtes un générateur
        pour faire cette récursion vous permettra
        d'ajouter pleins de ITaskEditorDisplayableObject,
        d'un coup, en tant que sous branche de la dernière créée.
        """
        raise NotImplementedError
    def getColor(self):
        raise NotImplementedError