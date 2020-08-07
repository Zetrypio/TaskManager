# -*- coding:utf-8 -*-

class GroupeManager():
    """
    Gestionnaire de groupes.
    Il y en a un par période.
    """
    def __init__(self, app, periode):
        """
        Constructeur du gestionnaire de groupes.
        @param app: Référence vers l'application.
        @param periode: Période qui contient
        ce gestionnaire de groupes.
        """
        self.__app = app
        self.__periode = periode
        self.__groupes = set()

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        """
        Getter de l'Application
        @return l'Application
        """
        return self.__app

    def getGroupes(self):
        """
        Permet d'obtenir les groupes gérés par ce gestionnaire de groupes.
        @return: une copie de l'ensemble des groupes de ce gestionnaire de groupes.
        """
        return self.__groupes.copy()

    def getPeriode(self):
        """
        Getter de la période.
        @return la période de ce gestionnaire de groupes.
        """
        return self.__periode

    ""
    #############################################
    # Méthodes liées à la gestion des groupes : #
    #############################################
    ""
    def ajouter(self, groupe):
        """
        Permet d'ajouter un groupe à la liste des groupes.
        @param groupe: le groupe à ajouter.
        """
        self.__groupes.add(groupe)
        self.__periode.addPrimitiveSchedulable(groupe)
#        self.getApplication().getDonneeCalendrier().updateAffichage()
#        self.getApplication().getTaskEditor().ajouter(groupe)

    def supprimer(self, groupe):
        """
        Permet de supprimer un groupe de la liste des groupes.
        @param groupe: le groupe à supprimer.
        """
        self.__groupes.remove(groupe)
        self.getApplication().getTaskEditor().supprimer(groupe)
        self.getApplication().getDonneeCalendrier().removeSchedulable(groupe)
        self.getApplication().getDonneeCalendrier().updateAffichage()
