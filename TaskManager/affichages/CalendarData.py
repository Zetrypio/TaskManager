# -*- coding:utf-8 -*-

class CalendarData:
    """
    Cette classe va regrouper les informations de p�riode,
    d'heures, des objets planifiables mis dans les calendriers.
    
    L'objectif est que modifier la date de d�but/fin de la p�riode
    en cours par exemple, n'ai pas besoin d'�tre ex�cut� sur tout
    les modes d'affichages comme on faisait jusqu'� maintenant
    via la classe DonneeCalendrier. Modifier quelque part
    sera de facto une modification de partout, car tout les
    affichages auront ces donn�es dans la m�me instance de cette classe.
    """
    def __init__(self):
        """
        Constructeur de CalendarData.
        Voir CalendarData.__doc__ pour la raison de cette classe.
        """
        pass