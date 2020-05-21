# *-* coding:utf-8 *-*

class GroupeManager():
    def __init__(self, periode):
        self.periode = periode
        self.groupes = set()

    def ajouter(self, Groupe):
        """ Créer un groupe et l'ajoute dans la liste """
        self.groupes.add(Groupe)

    def getPeriode(self):
        """ Getter de la période """
        return self.periode

    def getGroupes(self):
        """ Getter des groupes sur une période """
        return self.groupes
