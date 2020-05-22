# -*- coding:utf-8 -*-
from .task.ITaskEditorDisplayableObject import *

class AbstractSchedulableObject(ITaskEditorDisplayableObject):
    """
    Classe permettant la généralisation de Task et Group.
    """
    def __init__(self, nom, periode, desc="", color="white"):
        """
        @param nom     : nom de l'objet.
        @param periode : période de l'objet.
        @param desc    : description de l'objet.
        @param color   : texte désignant une couleur compatible avec les noms tkinter.
        """
        self.__nom      = nom
        self.__periode  = periode
        self.__desc     = desc
        self.__color    = color
        
        self.__selected = False
        self.__visible  = True

        self._statut    = ""

    "" # Marque pour que le repli de code fasse ce que je veux

    ############
    # Getters: #
    ############
    def getNom(self):
        return self.__nom

    def getPeriode(self):
        return self.__periode

    def getDescription(self):
        return self.__desc

    def getColor(self):
        return self.__color

    def getStatut(self):
        self.updateStatut()
        return self._statut

    def isSelected(self):
        """Permet de savoir si cet objet est sélectionné"""
        return self.__selected

    def isVisible(self):
        """Permet de savoir si cet objet est visible."""
        return self.__visible

    def getRepartition(self, displayedCalendar):
        raise NotImplementedError

    ""
    ############
    # Setters: #
    ############
    def setNom(self, nom):
        self.__nom = nom
    
    def setPeriode(self, periode):
        self.__periode = periode
    
    def setDescription(self, desc):
        self.__desc = desc
    
    def setColor(self, color):
        self.__color = color

    def setSelected(self, selected):
        """Permet de sélectionner ou déselectionner cet objet."""
        if not isinstance(selected, bool): raise TypeError("Exptected a boolean")
        self.__selected = selected

    def inverseSelection(self):
        """Permet d'inverser l'état de sélection."""
        self.selected = not self.selected

    def setVisible(self, visible):
        """Permet de rendre cet objet visible ou invisible."""
        if not isinstance(visible, bool): raise TypeError("Exptected a boolean")
        self.__visible = visible

    ""
    #####################
    # Clone and delete: #
    #####################
    def delete(self, app):
        """
        Permet de supprimer l'objet.
        @param app: Référence vers l'application pour obtenir les différents
        endroits qui doivent être au courrant que cet objet est supprimé.
        """
        raise NotImplementedError
    
    def copy(self):
        """
        Permet de copier cet objet.
        @return une copie de cet objet.
        """
        raise NotImplementedError

    ""
    ####################
    # Autre méthodes : #
    ####################
    def getFilterStateWith(self, filter):
        
        # TODO : À modifier
        
        # Si non autorisé par le filtre :
        if ("name" in filter and self.nom.lower().count(filter["name"]) == 0)\
        or ("type" in filter and not "Tâche" in filter["type"]): # TODO : Ajouter tâches indépendantes.
            return -1
        # Filtre prioritaire ?
        if "name" in filter and self.nom.lower().startswith(filter["name"].lower()):
            return 1
        # Sinon : autorisé par le filtre, mais pas prioritaire.
        return 0

    def updateStatut(self):
        """
        Permet de mettre à jour l'attribut statut.
        """
        raise NotImplementedError

    def createDisplayableInstance(self, frame, part):
        """
        Permet de créer une instance de la variante affichable de cet objet.
        @param frame: Le Frame dans lequel mettre l'instance.
        @param part: La partie à afficher si nécéssaire (pour les groupes par exemple).
        @return une instance de la classe représentant la variante affichable de cet objet.
        """
        raise NotImplementedError



