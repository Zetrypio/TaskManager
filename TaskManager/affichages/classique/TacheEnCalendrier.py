# -*- coding:utf-8 -*-
from ..AbstractDisplayedTask import *

class TacheEnCalendrier(AbstractDisplayedTask):
    def __init__(self, master, task, **kwargs):
        super().__init__(master, task, **kwargs)
        # Note : self.master est une référence vers le frame intérieur à AffichageCalendrier

    def getCalendrier(self):
        return self.master.master
    
