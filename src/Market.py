import math
from Ordine import *

class Market:
    #costruttore
    def __init__(self,id_mrk):
        self.id_mrk=id_mrk
        self.ordini=[]
        self.titoli=[]
        self.lock=False
    #imposta l'id del Maeket
    def set_id_mrk(self, value):
        self.id_mrk=value
    #aggiunge un titolo su cui operare
    def add_ttl(self,titolo):
        self.titoli.append(titolo)
    #aggiunge un ordine
    def add_order(self, ordine):
        self.ordini.append(ordine)
    #associa l'Event generator
    def set_event(self, evnt):
        self.event=evnt
    #in caso di evento blocca l'aggiornamento normale del market
    def update_evnt(self, titolo, event):
        for t in self.titoli:
            if event!=0 and t.get_id_ttl()==titolo.get_id_ttl():
                t.set_value(t.get_value()+event)
                self.lock=True
                
    #restituisce il valore di un determinato titolo su cui opera    
    def get_price(self, id_ttl):
        for t in self.titoli:
            if t.id_ttl==id_ttl:
                return t.get_value()
    #restituisce l'id del market su cui opera
    def get_id_mrk(self):
        return self.id_mrk
    #distanza tra due prezzi
    def distance(self, value, prezzo):
        if value==prezzo:
            return 1
        return math.fabs(1/float(value-prezzo))
    #calcola il massimo numero di azioni scambiate per un determinato valore v1
    def qta_exe(self, value):
        tmpSell=0
        tmpBuy=0
        maxCvalue=0
        maxAct=0
        for o in self.ordini:
                    
            if (o.get_state()=="Da processare") and value==o.get_prz() and o.get_id_ttl()==t.get_id_ttl():
                if o.get_qta()>0:
                    tmpSell+=o.get_qta()
                else:
                    tmpBuy+=o.get_qta()
        if min(tmpSell,abs(tmpBuy))>maxAct:
            maxAct=min(tmpSell,abs(tmpBuy))
            maxCvalue=v
        return maxAct
    #aggiorna il prezzo del titolo per rendere massimo di scambi possibili
    def update_tit_val(self):
        value=[]
        tmpSell=0
        tmpBuy=0
        maxCvalue=0
        maxAct=0
        for t in self.titoli:
            for o in self.ordini:
                if (o.get_id_ttl() == t.get_id_ttl()) and (o.get_state()=="Da processare"):
                    value.append(o.get_prz())
            value=set(value)
            for v in value:
                tmpSell=0
                tmpBuy=0
                for o in self.ordini:
                   
                    if (o.get_state()=="Da processare") and v==o.get_prz() and o.get_id_ttl()==t.get_id_ttl():
                        if o.get_qta()>0:
                            tmpSell+=o.get_qta()
                        else:
                            tmpBuy+=o.get_qta()
                if min(tmpSell,abs(tmpBuy))>maxAct:
                    maxAct=min(tmpSell,abs(tmpBuy))
                    maxCvalue=v
            if maxCvalue!=0:
                t.set_value(maxCvalue)
                print "prezzo titolo "+ str(t.get_value())
        return maxAct

    #calcola il valore del titolo ottimale per numero di scambi
    def get_maxCvalue(self):
        value=[]
        tmpSell=0
        tmpBuy=0
        maxCvalue=0
        maxAct=0

        for t in self.titoli:
            for o in self.ordini:

                if (o.get_id_ttl() == t.get_id_ttl()) and (o.get_state()=="Da processare"):
                    value.append(o.get_prz())
            value=set(value)
            for v in value:
                tmpSell=0
                tmpBuy=0
                for o in self.ordini:

                    if (o.get_state()=="Da processare") and v==o.get_prz() and o.get_id_ttl()==t.get_id_ttl():
                        if o.get_qta()>0:
                            tmpSell+=o.get_qta()

                        else:
                            tmpBuy+=o.get_qta()
 
                if min(tmpSell,abs(tmpBuy))>maxAct:
                    maxAct=min(tmpSell,abs(tmpBuy))
                    maxCvalue=v
        return maxCvalue

    #calcola il massimo numero di azioni scambiate per un determinato valore v2
    def get_maxAct(self, prz):
        value=[]
        tmpSell=0
        tmpBuy=0
        maxCvalue=0
        maxAct=0

        for t in self.titoli:
            for o in self.ordini:

                if (o.get_id_ttl() == t.get_id_ttl()) and (o.get_state()=="Da processare"):
                    value.append(o.get_prz())
            value=set(value)
            for v in value:
                tmpSell=0
                tmpBuy=0
                for o in self.ordini:
                    
                    if (o.get_state()=="Da processare") and v==prz and o.get_id_ttl()==t.get_id_ttl():
                        if o.get_qta()>0:
                            tmpSell+=o.get_qta()
                        else:
                            tmpBuy+=o.get_qta()
                if min(tmpSell,abs(tmpBuy))>maxAct:
                    maxAct=min(tmpSell,abs(tmpBuy))
                    maxCvalue=v
        return maxAct

    #accorpa gli ordini eseguiti dagli stessi agenti
    def accorpa_ord(self):
        for o in self.ordini:
            for o2 in self.ordini:
                if o.get_id_es()==o2.get_id_es() and o.get_prz()==o2.get_prz() and o2.get_state()!="Old" and o.get_state()!="Old" and o.to_string()!=o2.to_string():
                    o.set_qta(o.get_qta()+o2.get_qta())
                    o2.set_state("Old")
    #chiamata dall'esterno, aggiorna l'intero Market
    def update(self):
        ob=[]
        self.accorpa_ord()
        
        #Rimozioni ordini eseguiti
        for o in self.ordini:
            if o.state=="Eseguito" or o.state=="Old":
                ob.append(o)
        for o in ob:
            self.ordini.remove(o)
        
        for t in self.titoli:
            if self.lock==False:

                maxAct=self.update_tit_val()
            else:
                maxAct=self.get_maxAct(t.get_value())
            self.exe_ord(maxAct)
        self.lock=False
    #aggiorna il market tenendo conto degli eventi
    def ltl_update(self):
        ob=[]
        self.accorpa_ord()
        
        #Rimozioni ordini eseguiti
        for o in self.ordini:
            if o.state=="Eseguito" or o.state=="Old":
                ob.append(o)
        for o in ob:
            self.ordini.remove(o)
            
        for t in self.titoli:
            maxAct=self.get_maxAct()
            self.exe_ord(maxAct)

    #esegue gli ordini per il prezzo trovato
    def exe_ord(self, maxAct):
        maxActP=0
        maxActN=0
        #Esegue gli scambi al valore trovato
        for t in self.titoli:
            maxActP=maxAct
            maxActN=maxAct
            for o in self.ordini:
                if o.get_prz()==t.get_value() and (o.get_state()=="Da processare") and maxActP+maxActN>0:

                    if o.get_qta()>0:
                        if maxActP>=o.get_qta():
                            o.set_qta_eff(o.get_qta())
                            maxActP-=o.get_qta()
                            o.set_qta(0)
                            
                        else:
                            o.set_qta_eff(maxActP)
                            o.set_qta(o.get_qta()-maxActP)
                            maxActP=0
                    else:
                        if maxActN>=abs(o.get_qta()):
                            o.set_qta_eff(o.get_qta())
                            maxActN+=o.get_qta()
                            o.set_qta(0)
                        else:
                            o.set_qta_eff(0-maxActN)
                            o.set_qta(o.get_qta()+maxActN)
                            maxActN=0
                    if o.get_qta()==0:
                        o.set_state("Eseguito")

