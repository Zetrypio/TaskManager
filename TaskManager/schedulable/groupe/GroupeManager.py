# -*- coding:utf-8 -*-

class GroupeManager():
    def __init__(self, app, periode):
        self.__app = app
        self.__periode = periode
        self.__groupes = set()

    def ajouter(self, groupe):
        """ Créer un groupe et l'ajoute dans la liste """
        self.__groupes.add(groupe)
        self.__app.getDonneeCalendrier().getPanneauActif().updateAffichage()
        self.__app.getTaskEditor().ajouter(groupe)

    def getPeriode(self):
        """ Getter de la période """
        return self.__periode

    def getGroupes(self):
        """ Getter des groupes sur une période """
        return self.__groupes
