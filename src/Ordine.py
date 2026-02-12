import datetime
import math
import random
class Ordine:
    #costruttore
    def __init__(self, id_es, num_ord, id_ttl, qta, prezzo):
        self.id_es=id_es
        self.num_ord=num_ord
        self.id_ttl=id_ttl
        self.qta=qta
        self.qta_eff=0
        self.prezzo=prezzo
        now = datetime.datetime.now()
        self.date=str(now.day)+"/"+str(now.month)+"/"+str(now.year)+"  "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        self.state='Da processare'
    def set_state(self, state):
        self.state=state
    def get_state(self):
        return self.state
    def set_state(self, value):
        self.state=value
    def get_id_ttl(self):
        return self.id_ttl

    def get_id_es(self):
        return self.id_es
    def get_num_ord(self):
        return self.num_ord
    def get_date(self):
        return self.date
    def get_qta(self):
        return self.qta
    def get_qta_eff(self):
        return self.qta_eff
    def set_qta(self, value):
        self.qta=value
    def set_qta_eff(self, value):
        self.qta_eff=value
    def get_prz(self):
        return self.prezzo
    #stampa i dati dell'ordine
    def to_string(self):
        return "Id ordine: "+self.id_es+"-"+str(self.num_ord)+" Id Titolo: "+self.id_ttl+" Qta: "+str(self.qta)+" Qta Eff: "+str(self.qta_eff)+" Prezzo: "+str(self.prezzo) + " Stato: "+self.state

