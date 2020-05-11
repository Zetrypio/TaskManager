# *-* coding:utf-8 *-*

class Groupe():
    def __init__(self, nom, listTasks, color, periode, GroupeManager):
        self.nom           = nom
        self.color         = color
        self.periode       = periode
        self.groupeManager = GroupeManager

        self.listTasks = set()
        for tache in listTasks:
            self.listTasks.add(tache)

        self.select = False

    def getNom(self):
        """ Getter du nom """
        return self.nom

    def getColor(self):
        """ Getter de la couleur """
        return self.color

    def getPeriode(self):
        """ Getter de la période """
        return self.periode

    def getListTasks(self):
        """ Getter des taches de la période """
        return self.listTasks

    def getGroupeManager(self):
        return self.groupeManager

    def getPeriode(self):
        """ Getter de la période du groupe """
        return self.getGroupeManager().getPeriode()

    def setNom(self, nom):
        """ Setter du nom """
        self.nom = nom

    def setColor(self, color):
        """ Setter de la couleur du groupe """
        self.color = color

    def setPeriode(self, periode):
        """ Setter de la periode lié au groupe """
        self.periode = periode

    def setSelect(self, value):
        """ Setter de la sélection d'un groupe """
        if not isinstance(value, bool): raise TypeError("Exptected a boolean")
        self.select = value

    def setGroupeManager(self, GroupeManager):
        """ Setter du groupe Manager """
        self.groupeManager = GroupeManager

    def addTask(self, task):
        """ Ajoute une task à la liste du groupe """
        self.listTasks.add(task)

    def removeTask(self, task):
        """ Retire une tache de la liste du groupe """
        self.listTasks.remove(task)

    def isSelected(self):
        """ Getter de la la variable de selection """
        return self.select

