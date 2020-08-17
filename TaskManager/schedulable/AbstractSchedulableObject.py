# -*- coding:utf-8 -*-
from .task.ITaskEditorDisplayableObject import *

from util.util import adaptTextColor

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
        self.__nom       = nom
        self.__periode   = periode
        self.__desc      = desc
        self.__color     = color

        self.__selected  = False
        self.__visible   = True

        self._statut     = ""

    "" # Marque pour que le repli de code fasse ce que je veux
    ############
    # Getters: #
    ############
    ""
    def getApplication(self):
        """
        Getter pour l'Application
        @return <Application>
        """
        return self.getPeriode().getApplication()

    def getColor(self):
        """
        Getter pour la couleur de cet objet pour l'affichage.
        Notez bien que c'est la couleur native, et que la sélection
        def cet objet ne changera en rien la couleur renvoyée ici.
        @return la couleur de cet objet.
        """
        return self.__color

    def getData(self):
        """
        Getter pour le data
        @return <Data>
        """
        return self.getApplication().getData()

    def getDescription(self):
        """
        Permet d'obtenir la description de l'objet
        qui a été donné par l'utilisateur lors de
        sa création. (ou changé après TODO).
        @return la description de cet objet.
        """
        return self.__desc

    def getFilterStateWith(self, filter):
        """
        Permet de savoir l'état de filtrage de cet objet selon le filtre donné
        lors de l'affichage de cet objet dans le Treeview() du TaskEditor().
        @param filter: Dictionnaire du filtre.
        @return -1 si l'élément n'est pas filtré, 1 si il est prioritaire, et 0 sinon.
        @specified by getFilterStateWith(filter) in ITaskEditorDisplayableObject().
        """

        # TODO : À modifier

        # Si non autorisé par le filtre :
        if ("name" in filter and self.__nom.lower().count(filter["name"]) == 0)\
        or ("type" in filter and not "Tâche" in filter["type"]): # TODO : Ajouter tâches indépendantes.
            return -1
        # Filtre prioritaire ?
        if "name" in filter and self.__nom.lower().startswith(filter["name"].lower()):
            return 1
        # Sinon : autorisé par le filtre, mais pas prioritaire.
        return 0

    def getFirstPart(self, displayedCalendar):
        """
        Getter pour obtenir la première part affichée de #getRepartition(displayedCalendar).
        @param displayedCalendar: Nécessaire pour savoir l'obtenir parmi celle qui sont réellement affichables.
        @return la première datetimeItemPart affichée parmi toutes.
        """
        for part in self.getRepartition(displayedCalendar):
            return part

    def getLastPart(self, displayedCalendar):
        """
        Getter pour obtenir la dernière part affichée de #getRepartition(displayedCalendar).
        @param displayedCalendar: Nécessaire pour savoir l'obtenir parmi celle qui sont réellement affichables.
        @return la dernière datetimeItemPart affichée parmi toutes.
        """
        for part in self.getRepartition(displayedCalendar):
            pass
        return part

    def getNom(self):
        """
        Getter pour le nom de l'objet planifiable.
        Le nom n'est évidemment pas celui de la classe,
        mais bien celui donné par l'utilisateur.
        @return le nom de l'objet.
        """
        return self.__nom

    def getPeriode(self):
        """
        Permet d'obtenir la période de cet objet.
        @return la période de cet objet.
        """
        return self.__periode

    def getRawRepartition(self, displayedCalendar):
        """
        Permet d'obtenir toutes les DatetimeItemParts
        nécessaire à l'affichage de cet objet, de manière brute,
        c'est-à-dire sans fusion des parties qui pourraient l'être.
        (notamment pour les groupes par exemple).
        Cette méthode sera appelée avant l'affichage pour une
        précalculation de ce qui doit être affiché.
        Nécessaire pour savoir si des DatetimeItemParts sont
        fusionnable.
        Les datetimeItemParts doivent avoir self dans l'attribut
        schedulable passé via le constructeur de ces parts.
        (enfin ça c'est si vous voulez les retrouver dans la méthode
        self.getRepartition() =) ).
        
        @param displayedCalendar: Permettra de couper les parts
        selon ce qui sera réellement affichable.

        @return un itérable (générateur ou autre) de DatetimeItemParts
        contenant toutes les parts non fusionnées nécessaires à l'affichage
        de cet objet.
        """
        raise NotImplementedError

    def getRepartition(self, displayedCalendar):
        """
        Permet d'avoir toutes les DatetimeItem Parts nécessaire
        à l'affichage de cet objet, mais de manière fusionné si
        vous en avez envie. Cette méthode est appelée après
        que tout les AbstractSchedulableObject aient appelés
        la méthode self.getRawRepartition().
        
        @param displayedCalendar: Permettra de couper les parts
        selon ce qui sera réellement affichable.

        @return un itérable (générateur ou autre) de DatetimeItemParts
        contenant toutes les parts éventuellement fusionnées si
        vous en avez envie, nécessaires à l'affichage de cet objet.
        """
        raise NotImplementedError

    def getStatut(self):
        """
        Permet de mettre à jour et obtenir le statut.
        @return le statut de cet objet.
        """
        self.updateStatut()
        return self._statut

    def isSelected(self):
        """
        Permet de savoir si cet objet est sélectionné
        @return True si l'objet est sélectionné.
        @return False si l'objet n'est pas sélectionné.
        """
        return self.__selected

    def isVisible(self):
        """
        Permet de savoir si cet objet est visible.
        @return True si l'objet est visible.
        @return False si l'objet est invisible.
        """
        return self.__visible

    ""
    ############
    # Setters: #
    ############
    ""
    def inverseSelection(self):
        """
        Permet d'inverser l'état de sélection.
        Si l'objet était sélectionné, il ne le sera plus
        et inversement.
        """
        self.__selected = not self.__selected

    def setColor(self, color):
        """
        Setter pour la couleur de cet objet,
        doit être un nom compatible avec les couleurs tkinter.
        @param color: la couleur à mettre, sous forme de texte
        au format tkinter.
        """
        self.__color = color

    def setDescription(self, desc):
        """
        Setter pour la description de cet objet,
        celle qui est donnée par l'utilisateur.
        @param desc: la description à mettre, sous forme de texte.
        """
        self.__desc = desc
    def setNom(self, nom):
        """
        Setter pour le nom donné par l'utilisateur de cet objet.
        @param nom: le nom à mettre, sous forme de texte.
        """
        self.__nom = nom
    
    def setPeriode(self, periode):
        """
        Setter pour la période de cet objet.
        Cette méthode ne change rien dans la période en question.
        @param periode: la période à mettre.
        """
        if self.getPeriode() != periode:
            self.getPeriode().removePrimitiveSchedulable(self)
            self.getPeriode().removeInstanciatedSchedulable(self)
            self.__periode = periode
            periode.addPrimitiveSchedulable(self)

    def setPeriodeWithName(self, name):
        """
        Setter pour la période
        @param name : <str> nom de la période
        """
        for p in self.getApplication().getPeriodManager().getPeriodes():
            if p.getNom() == name:
                self.setPeriode(p)
                break

    def setSelected(self, selected):
        """
        Permet de sélectionner ou désélectionner cet objet.
        @param selected: True si l'objet doit être sélectionné, False sinon.
        """
        if not isinstance(selected, bool): raise TypeError("Exptected a boolean")
        self.__selected = selected

    def setVisible(self, visible):
        """
        Permet de rendre cet objet visible ou invisible.
        @param visible: True si l'objet doit être visible, False sinon. 
        """
        if not isinstance(visible, bool): raise TypeError("Exptected a boolean")
        self.__visible = visible

    ""
    #####################
    # Clone and delete: #
    #####################
    ""
    def instantiate(self):
        """
        Permet d'ajouter la version instanciée de l'objet à la période.
        L'idée est d'appeler la méthode self.getPeriode().addInstantitatedSchedulable()
        pour y ajouter ce que doivent afficher les calendriers (en tâches séparées contrairement
        à #getRepartition() ou #getRawRepartition()).
        """
        raise NotImplementedError

    def copy(self):
        """
        Permet de copier cet objet.
        @return une copie de cet objet.
        """
        raise NotImplementedError

    def delete(self, app):
        """
        Permet de supprimer l'objet.
        @param app: Référence vers l'application pour obtenir les différents
        endroits qui doivent être au courant que cet objet est supprimé.
        """
        raise NotImplementedError

    ""
    ####################
    # Autre méthodes : #
    ####################
    ""
    def acceptLink(self):
        """
        Permet de savoir si l'objet peut être à l'origine d'un lien, sans se soucier
        de la destination pour le moment encore inconnu.
        @return True si l'objet est en capacité de faire des liens, False sinon.
        """
        raise NotImplementedError

    def acceptLinkTo(self, schedulable):
        """
        Permet de savoir si un lien est possible entre cet objet et l'objet reçu, peu importe le sens,
        peu importe si le lien existe déjà.
        @param schedulable: l'autre objet dont on doit faire le lien avec cet objet.
        """
        raise NotImplementedError

    def createDisplayableInstance(self, frame, part):
        """
        Permet de créer une instance de la variante affichable de cet objet.
        @param frame: Le Frame dans lequel mettre l'instance.
        @param part: La partie à afficher si nécessaire (pour les groupes par exemple).
        @return une instance de la classe représentant la variante affichable de cet objet.
        """
        raise NotImplementedError

    def updateStatut(self):
        """
        Permet de mettre à jour l'attribut statut.
        """
        raise NotImplementedError

    ""
    #######################################
    # Méthodes liées à l'enregistrement : #
    #######################################
    ""
    def saveByDict(self):
        """
        Méthode qui sauvegarde les attributs présent dans la super classe (ici)
        A redéfinir dans les sous-classe pour les nouveaux attributs

        @save nom     : <str> contient le nom de la tache
        @save periode : <str> contient le nom de la période
        @save desc    : <str> contient le texte de la description
        @save color   : <str> contient la couleur de la tache

        @return dico <dict> contient les couples clé-valeur ci-dessus
        """
        return {
            "nom"     : self.getNom(),
            "periode" : self.getPeriode().getNom(),
            "desc"    : self.getDescription(),
            "color"   : self.getColor()
        }
