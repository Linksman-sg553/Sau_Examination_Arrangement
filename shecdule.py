# -*- coding: UTF-8 -*-
import pymysql
class shecdule_modle:
    time = ''

class shecdule_list:
    list_shecdule = [shecdule_modle()]
    def push_pack(self, shecdule: shecdule_modle):
        self.list_shecdule.append(shecdule)