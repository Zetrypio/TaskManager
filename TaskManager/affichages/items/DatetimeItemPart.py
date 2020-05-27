# -*- coding:utf-8 -*-
import datetime

class DatetimeItemPart:
    """
    Méthode représentant une portion de temps,
    en l'occurence une portion de tâche, groupe ou autres.
    Une datetimeItemPart ne peut être présent que sur un seul jour.
    """
    def __init__(self, jour, heureDebut, heureFin, schedulable):
        assert isinstance(jour,       datetime.date)
        assert isinstance(heureDebut, datetime.time)
        assert isinstance(heureFin,   datetime.time)
        self.__heureDebut  = heureDebut
        self.__heureFin    = heureFin
        self.__jour        = jour
        self.__schedulable = schedulable
    
    def getDebut(self):
        return datetime.datetime.combine(self.__jour, self.__heureDebut)
    
    def getFin(self):
        return datetime.datetime.combine(self.__jour, self.__heureFin)
    
    def getHeureDebut(self):
        return self.__heureDebut
    
    def getHeureFin(self):
        return self.__heureFin

    def getJour(self):
        return self.__jour + datetime.timedelta()

    def getSchedulable(self):
        return self.__schedulable
    
    def intersectWith(self, other):
        return self.getJour() == other.getJour() and\
            not (other.getHeureDebut() > self.getHeureFin()
              or other.getHeureFin()  <  self.getHeureDebut())
