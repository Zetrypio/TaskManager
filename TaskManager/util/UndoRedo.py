# -*- coding:utf-8 -*-
import traceback, sys

class UndoRedo:
    """
    Gestionnaire de Undo-Redo.
    Les instances sont les éléments des stacks d'Undo-Redo.
    Ce sont des objets qui ont 2 fonctions pour faire l'undo et le redo.
    Les stacks d'undo-redo sont les attributs statiques de cette classe.
    """
    UNDO = []
    REDO = []

    def __init__(self, action = None, autoAdd = True, **info):
        """
        Constructeur d'un élément du stack de l'Undo-Redo.
        @param action: Nom de l'action pour l'affichage.
        @param autoAdd = True: Si sur True, rajoute automatiquement cet objet au gestionnaire d'undo-redo.
        @param **info: Autres informations nécessaire pour le undo-redo.
        """
        self.action = action
        self.info = info
        if autoAdd:
            self.addToStack()

    def addToStack(self):
        """
        Permet d'ajouter l'undoRedo à la pile d'UndoRedo s'il n'est pas déjà présent.
        Il se rajoute automatiquement au constructeur si non explicitement précisé qu'il ne faut pas.
        """
        if not self in UndoRedo.UNDO + UndoRedo.REDO:
            UndoRedo.UNDO.append(self)
            UndoRedo.REDO = []

    def _undo(self):
        """
        Méthode à redéfinir dans les sous-classes pour faire l'undo.
        """
        raise NotImplementedError

    def _redo(self):
        """
        Méthode à redéfinir dans les sous-classes pour faire l'redo.
        """
        raise NotImplementedError

    def __do(self, mode):
        """
        Méthode qui exécute Undo ou Redo en conséquence de ce qui est demandé.
        """
        try:
            if mode == "undo":
                self._undo()
            elif mode == "redo":
                self._redo()
        except:
            sys.stderr.write("Exception in %s callback :\n"%mode)
            traceback.print_exc()

    @staticmethod
    def undo():
        """
        Permet de faire un undo de manière globale.
        """
        if UndoRedo.UNDO:
            u = UndoRedo.UNDO.pop()
            u.__do(mode = "undo")
            UndoRedo.REDO.append(u)

    @staticmethod
    def redo():
        """
        Permet de faire un redo de manière globale.
        """
        if UndoRedo.REDO:
            r = UndoRedo.REDO.pop()
            r.__do(mode = "redo")
            UndoRedo.UNDO.append(r)

    @staticmethod
    def addSimple(undoFunc, redoFunc, action, autoAdd = True, **info):
        """
        Permet de rajouter un couple de fonctions simplement pour l'undo redo.
        @param undoFunc: la fonction à exécuter pour undo.
        @param redoFunc: la fonction à exécuter pour redo.
        @param action: Nom de l'action pour l'affichage.
        @param autoAdd = True: Si sur True, rajoute automatiquement cet objet au gestionnaire d'undo-redo.
        @param **info: Autres informations nécessaire pour le undo-redo.
        """
        ur = UndoRedo(action, autoAdd, **info)
        ur._undo = undoFunc
        ur._redo = redoFunc

    @staticmethod
    def reset():
        UndoRedo.UNDO = []
        UndoRedo.REDO = []
