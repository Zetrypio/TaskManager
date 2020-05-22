# -*- coding:utf-8 -*-
import datetime

class DatetimeItemPart:
    """
    Méthode représentant une portion de temps,
    en l'occurence une portion de tâche, groupe ou autres.
    Une datetimeItemPart ne peut être présent que sur un seul jour.
    """
    def __init__(self, jour, heureDebut, heureFin):
        assert isinstance(jour,       datetime.date)
        assert isinstance(heureDebut, datetime.time)
        assert isinstance(heureFin,   datetime.time)
        self.__jour       = jour
        self.__heureDebut = heureDebut
        self.__heureFin   = heureFin
    
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
    
    def instersectWith(self, other):
        return self.__jour == other.__jour and not (other.__debut > self.__fin or other.__fin < self.__debut)
