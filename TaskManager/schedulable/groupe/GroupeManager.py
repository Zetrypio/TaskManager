# -*- coding:utf-8 -*-

class GroupeManager():
    """
    Gestionaire de groupes.
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

    def ajouter(self, groupe):
        """
        Permet d'ajouter un groupe à la liste des groupes.
        @param groupe: le groupe à ajouter.
        """
        self.__groupes.add(groupe)
        self.__app.getDonneeCalendrier().getPanneauActif().updateAffichage()
        self.__app.getTaskEditor().ajouter(groupe)

    def getPeriode(self):
        """
        Getter de la période.
        @return la période de ce gestionnaire de groupes.
        """
        return self.__periode

    def getGroupes(self):
        """
        Permet d'obtenir les groupes gérés par ce gestionnaire de groupes.
        @return: une copie de l'ensemble des groupes de ce gestionnaire de groupes.
        """
        return self.__groupes.copy()
