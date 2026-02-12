# -*- coding: cp1252 -*-

from Ordine import *
from Event_generator import *
from Titolo import *
import random

class Agente:
    #variabili di classe per l'aggiotaggio
    agg_list=[]
    agg_stt=[]
    agg_stt.append("Idle")
    agg_qta=[]
    agg_qta.append(0)
    agg_prz=[]
    agg_prz.append(0)
    agg_ord=[]
    agg_num_inv=[]
    agg_num_inv.append(0)
    agg_num_flw=[]
    agg_num_flw.append(0)
    #costruttore
    def __init__(self, id_agn,typ_agn, budget, tnd_rsc, market, agn_str):
        self.evG=Event_generator()
        self.id_agn=id_agn #identificativo agente
        self.typ_agn=typ_agn #tipologia di agente
        self.budget=budget #capitale a disposizione
        self.liquidita=budget #liquidità disponibile
        self.qta_azn=[] #quantita di azioni possedute
        self.prz_azn=[] #valore di aquisto delle azionei *(1)
        self.tnd_rsc=tnd_rsc #valore di tendenza al rischio dell'agente
        self.market=market #mercato su cui si opera
        self.count_ord=0 #numero di ordini effettuati
        self.count=0 #ordini attivi (da eseguire)
        self.ordini=[] #ordini creati ancora attivi
        self.portfolio=[] #titoli su cui si opera
        self.agn_str=agn_str #numero della strategia che l'agente andrà ad applicare
        self.gain=0 #guadagno dell'agente
    	####VARIABILI di DECISIONE####
        self.wait_t=0 #tempo di attesa *(2)
        self.inv=0 #quantità di denaro investita
        self.list_v=[]
        self.s03_flag=0
        self.s04_flag=False
        self.act=False
        self.next=0
        self.sig="+"
        self.stmp=0
        self.tprz=0
        self.agg_type=""
        if agn_str==7:
            
            self.agg_type=self.dec_type(self.id_agn)
            self.agg_list.append(self.id_agn+"-"+self.agg_type)
            if self.agg_type=="Inv":
                self.agg_num_inv[0]+=1
            else:
                self.agg_num_flw[0]+=1

    def get_id(self):
        return self.id_agn

    def get_gain(self):
        self.gain_calc()
        return self.gain

    def get_lqd(self):
        return self.liquidita

    def set_event(self, evg):
        self.evG=evg
    #assegna un tipo all'agente che pratica l'aggiotaggio
    def dec_type(self, id_agn):
        x=random.randint(0,100)
        if "t" in id_agn:
            if x<70:
                return "Inv"
        else:
            return "Flw"
        return "Flw"

    #crea l'ordine e lo invia al Market
    def mk_ord(self, id_ttl, qta, prz, agg):

        if (abs(qta*prz)<=self.budget) and (qta>=-20000):
            orda=Ordine(self.id_agn,self.count_ord, id_ttl,qta,prz)
            self.market.add_order(orda)
            self.count+=1
            self.count_ord+=1
            self.ordini.append(orda)
            if agg==True:
                self.agg_ord.append(orda)

    #aggiunge un titolo al portfolio (=lista di titoli su cui operare)
    def add_ttl(self,titolo):
        self.portfolio.append(titolo)

    #rimuove un ordine (non usata?)
    def remove_ord(self, id_ord):
        ob=Ordine("","",0,0)
        for o in self.ordini:
            if o.id_ord==id_ord:
                ob=o
                o.set_state("Eliminato")
                break
        if ob.id_ord!="":
            self.ordini.remove(ob)
    #rimuove gli ordini eseguiti
    def remove_old(self):
        ob=[]
        for o in self.ordini:
            if o.state=="Finito" or o.state=="Old":
                ob.append(o)
        for o in ob:
            self.ordini.remove(o)
    #restituisce l'indice per il vettore di azioni possedute che vendute al momento attuale fornisce il massimo guadagno
    def fnd_max_g(self, prz):
        g=-99999999
        index=0
        for i in range(len(self.prz_azn)):
            if (prz-self.prz_azn[i])*self.qta_azn[i]>g:
                g= (prz-self.prz_azn[i])*self.qta_azn[i]
                index=i
        return index
    #rimuove gli elementi del vettore di azioni possedute per i quali non si possiedono più azioni
    def rmv_zro(self):
        rm=[]
        for a in range(len(self.qta_azn)):
            if self.qta_azn[a]==0:
                rm.append(a)
        for r in rm:
            self.qta_azn.remove(self.qta_azn[r])
            self.prz_azn.remove(self.prz_azn[r])


          
    #aggiorna la quantita di azioni possedute in base agli ordini eseguiti sul Market
    def mcm_prz(self, prz, qta, o):
        flg=False
        tag=False
        index=-1       
        if len(self.prz_azn)==0:
            self.prz_azn.append(prz)
            self.qta_azn.append(qta)
            self.budget-=abs(o.get_prz()*o.get_qta_eff())#+1   
            self.inv+=abs(o.get_prz()*o.get_qta_eff())
        else:
            if (self.qta_azn[0]>0 and qta>0) or (self.qta_azn[0]<0 and qta<0):
                self.budget-=abs(o.get_prz()*o.get_qta_eff())
                self.inv+=abs(o.get_prz()*o.get_qta_eff())
                for i in range(len(self.prz_azn)):
                    if self.prz_azn[i]==prz:
                        self.qta_azn[i]+=qta
                        flg=True
                if flg==False:
                    self.prz_azn.append(prz)
                    self.qta_azn.append(qta)
            else:
                while(qta!=0):
                    if len(self.qta_azn)==0:
                        self.qta_azn.append(qta)
                        self.prz_azn.append(prz)
                        self.budget-=abs(o.get_prz()*(self.qta_azn[0]))#+1   
                        self.inv+=abs(o.get_prz()*self.qta_azn[0])
                        qta=0
                    else:
                        index=self.fnd_max_g(prz)
                        qta_exc=min(abs(qta), abs(self.qta_azn[index]))
                        if self.qta_azn[index]<0:
                            tag=True
                        if qta>0:
                            self.qta_azn[index]+=qta_exc
                            qta-=qta_exc
                        else:
                            self.qta_azn[index]-=qta_exc
                            qta+=qta_exc
                        if tag:
                            qta_exc=qta_exc*(-1)
                        tmp=abs(qta_exc)*self.prz_azn[index]+(prz-self.prz_azn[index])*qta_exc
                        self.budget+=tmp
                        self.inv-=abs(qta_exc)*self.prz_azn[index]
                        self.rmv_zro()
    #rende l'agente stampabile
    def to_string(self):
        agn_str="ID: "+str(self.id_agn)+" budget "+ str(float(self.budget)/10000)+" Investimento "+ str(float(self.inv)/10000)
        for i in range(len(self.qta_azn)):
            agn_str+=" qta: "+str(self.qta_azn[i])+ " prezzo: "+str(float(self.prz_azn[i])/10000)
        agn_str+=" gain "+ str(float(self.gain)/10000)
        return agn_str

    #aggiorna tutti i possedimenti dell'agente
    def update_value(self):
        self.gain=0
	#aggiorna la quantita posseduta e calcola il gain
        for o in self.ordini:
            if o.get_qta_eff()!=0:
                self.mcm_prz(o.get_prz(),o.get_qta_eff(),o)
                o.set_qta_eff(0)
                if o.get_state()=="Eseguito":
                    o.set_state("Finito")
                    self.count-=1
        if len(self.qta_azn)!=0:
            self.gain_calc()
        self.liquidita=self.gain+self.budget+self.inv
	#rimozioni ordini Eseguiti
        self.remove_old()

    
    def get_val_c(self, id_ttl): #restituisce il valore di un titolo al momento corrente
        for p in self.portfolio:
            if p.get_id_ttl()==id_ttl:
                return p.get_value()
        return 0

    #aggiorna il gain al momento corrente
    def gain_calc(self):
        for p in self.portfolio:
            for i in range(len(self.prz_azn)):
                self.gain+=(p.get_value()-self.prz_azn[i])*self.qta_azn[i]

    #applica la strategia
    def update_str(self):
        for p in self.portfolio:
            d=random.uniform(1, 100)
            if d>=10:
                if self.agn_str==1:
                    self.strategy01(p)
                if self.agn_str==2:
                    self.strategy02(p)
                if self.agn_str==3:
                    self.strategy03(p)
                if self.agn_str==4:
                    self.strategy04(p)
                if self.agn_str==5:
                    self.strategy05(p)
                if self.agn_str==6:
                    self.strategy06(p)
                if self.agn_str==7:
                    self.strategy07(p)
        self.ord_count=0
        for o in self.ordini:
            self.ord_count+=1

    #determina l'andamento del titolo	
    def andamento(self,lst):
        count=0
        i=1
        while i<len(lst):
            if lst[i-1]<lst[i]:
                count+=1
            if lst[i-1]>lst[i]:
                count-=1
            i+=1
        return count


    def max_ord(self):
        value=[]
        tmpSell=0
        tmpBuy=0
        maxCvalue=0
        maxAct=0
        for t in self.portfolio:
            for o in self.market.ordini:

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
        return str(maxAct)+" "+str(maxCvalue)

    
    #STRATEGIA 01 totalmente casuale
    def strategy01(self, titolo):
        if self.count<50:
            qta=(random.uniform(0,2*self.budget/100*self.tnd_rsc)-self.budget/100*self.tnd_rsc)/titolo.value
            price=random.uniform(int((titolo.value)-(self.tnd_rsc/2)),int((titolo.value)+(self.tnd_rsc/2))+2)
            self.mk_ord(titolo.id_ttl, int(qta),int(price), False)

    #STRATEGIA 02 guarda prima l'andamento del titolo e poi si comporta di conseguenza
    def strategy02(self, titolo):
        self.list_v.append(titolo.value)
        if len(self.list_v)>10:
            self.list_v.pop()
        time=20
        if self.wait_t==0:
            if len(self.qta_azn)==0:
                if len(self.list_v)>=10:
                    count=self.andamento(self.list_v)
                    if count>=1:
                        qta=random.uniform(5,self.budget/1000*self.tnd_rsc)/titolo.value
                        self.mk_ord(titolo.id_ttl,int(qta),titolo.get_value(),False)
                    if count<=-1:
                        qta=random.uniform(5,self.budget/1000*self.tnd_rsc)/titolo.value
                        self.mk_ord(titolo.id_ttl,int(0-qta),titolo.get_value(),False)
            else:
                self.strategy03(titolo)
        else:
            self.wait_t-=1

    #STRATEGIA 03 da una prima operazione casuale determina le successiva in base al gain
    def strategy03(self,titolo):
        x=0
        if len(self.qta_azn)==0:
            x=int(random.uniform(0, 10))
            if x>5:
                  self.strategy01(titolo)
            else:
                  self.strategy02(titolo)
        else:
            self.gain_calc()
            if self.gain>20:
                self.mk_ord(titolo.id_ttl, 0-self.qta_azn[0],titolo.get_value(),False)
                
    #STRATEGIA 04 per i top speculativa
    def strategy04(self,titolo):
        if len(self.qta_azn)==0:
            x=int(random.uniform(0, 10))
            if x>5:
                qta=random.uniform(5,self.budget/1000*self.tnd_rsc)/titolo.value
                self.mk_ord(titolo.id_ttl,int(qta),titolo.get_value(),False)
                self.s04_flag=True
            else:
                qta=random.uniform(5,self.budget/1000*self.tnd_rsc)/titolo.value
                self.mk_ord(titolo.id_ttl,int(0-qta),titolo.get_value(),False)
                self.s04_flag=False
        else:
            qta1=0-int(self.qta_azn[0]/3)
            qta2=0-self.qta_azn[0]+qta1
            if self.s04_flag==True:
                prz1=self.prz_azn[0]+8
                prz2=self.prz_azn[0]+10
            else:
                prz1=self.prz_azn[0]-8
                prz2=self.prz_azn[0]-10
                
            self.mk_ord(titolo.id_ttl,qta1,prz1,False)
            self.mk_ord(titolo.id_ttl,qta2,prz2,False)
            
    #STRATEGIA 05 analizzo gli ordini eseguiti e mi muovo di conseguenza (big)
    def strategy05(self, titolo):
        if len(self.qta_azn)==0:
            
            maxCvalue=self.market.get_maxCvalue()
            if maxCvalue>=titolo.get_value():
                qta=random.uniform(5,self.budget/1000*self.tnd_rsc)/titolo.value
                self.mk_ord(titolo.id_ttl,int(qta),titolo.get_value(),False)
            if maxCvalue<=titolo.get_value():
                qta=random.uniform(5,self.budget/1000*self.tnd_rsc)/titolo.value
                self.mk_ord(titolo.id_ttl,int(0-qta),titolo.get_value(),False)
        else:
            self.strategy03(titolo)
            

    #STRATEGIA 06 basata sulla conoscenza degli eventi futuri
    
    def strategy06(self, titolo):
        j=0
        i=0
        tmp=[]
        tmp=self.evG.oracle(5)
        if self.act==False:
            self.stmp=tmp[0]+tmp[1]+tmp[2]+tmp[3]+tmp[4]
            self.tprz=titolo.get_value()
            if self.stmp>8:
                qta=random.uniform(500,self.budget/100*self.tnd_rsc)/titolo.value
                self.mk_ord(titolo.id_ttl,int(qta),titolo.get_value(),False)
                self.sig="+"
                self.act=True
                self.wait_t=3
            if self.stmp<-8:
                qta=random.uniform(500,self.budget/100*self.tnd_rsc)/titolo.value
                self.mk_ord(titolo.id_ttl,int(0-qta),titolo.get_value(),False)
                self.sig="-"
                self.act=True
                self.wait_t=3
        else:
            if self.wait_t==0:
                qta=random.uniform(500,self.budget/100*self.tnd_rsc)/titolo.value
                if self.sig=="+":
                   self.mk_ord(titolo.id_ttl,0-qta,self.tprz+self.stmp,False)
                else:
                    self.mk_ord(titolo.id_ttl,qta,self.tprz+self.stmp,False)
                self.act=False
            else:
                self.wait_t-=1

            
    #restituisce il tipo dell'agente che pratica l'aggiotaggio
    def get_type(self):
        tmp=[]
        for i in range(len(self.agg_list)):
            if self.id_agn in self.agg_list[i]:
                tmp=self.agg_list[i].partition("-")
                return tmp[2]
        return "Not Found"    
    #restituisce lo stato degli ordini degli agenti che praticano l'aggiotaggio
    def ord_status(self, delta):
        for i in range(len(self.agg_ord)):
            if self.agg_ord[i].get_prz()==self.agg_prz[0]+delta:
                return True
        return False

    #STRATEGIA 07 aggiottaggio gli agenti comunicano tra loro
    agn_agg=[]
    agree=False
    agg_count_inv=[]
    agg_count_inv.append(0)
    agg_count_flw=[]
    agg_count_flw.append(0)
    agg_wait=[]
    agg_sign=[]
    agg_sign.append(".")
    agg_wait.append(0)
    def strategy07(self,titolo):
        if self.agg_qta[0]==0:
            self.agg_qta[0]=random.randint(100000,300000)
        if self.agg_wait[0]==0:
            if self.get_type()=="Inv":
                if self.agg_stt[0]=="Idle":
                    self.agg_count_inv[0]+=1
                    if len(self.agg_ord)==0:
                        qta_inv=int(self.agg_qta[0]/self.agg_num_inv[0])
                        self.mk_ord(titolo.id_ttl,int(qta_inv),titolo.get_value(),True)
                        self.agg_sign[0]="+"
                    self.agg_prz[0]=titolo.get_value()
                if self.agg_stt[0]=="1st":
                    self.agg_count_inv[0]+=1
                    if self.agg_sign[0]=="+":
                        qta_inv=int(self.agg_qta[0]/self.agg_num_inv[0])
                        self.mk_ord(titolo.id_ttl,int(0-qta_inv),self.agg_prz[0]+5,True)
                if self.agg_stt[0]=="2nd":
                    self.agg_count_inv[0]+=1
                    if self.agg_sign[0]=="+":
                        qta_inv=int(self.agg_qta[0]/self.agg_num_inv[0])
                        self.mk_ord(titolo.id_ttl,int(qta_inv),self.agg_prz[0]+8,True)
                if self.agg_stt[0]=="5th":
                    self.agg_count_inv[0]+=1
                    self.strategy04(titolo)              
            if self.get_type()=="Flw":
                if self.agg_stt[0]=="1st":
                    self.agg_count_flw[0]+=1
                    if self.agg_sign[0]=="+":
                        qta_inv=int(self.agg_qta[0]/self.agg_num_flw[0])
                        self.mk_ord(titolo.id_ttl,int(qta_inv),self.agg_prz[0]+5,True)

                        qta_inv=int(self.agg_qta[0]/self.agg_num_flw[0])
                        self.mk_ord(titolo.id_ttl,int(0-qta_inv),self.agg_prz[0]+8,True)
        else:
            self.agg_wait[0]-=1
        
        self.agg_update()

    #fa avanzare lo stato dell'aggiotaggio
    def agg_update(self):
        if self.agg_count_inv[0]==self.agg_num_inv[0]:
            if self.agg_stt[0]=="Idle":
                self.agg_stt[0]="1st"
                self.agg_count_inv[0]=0
                return 0
            
            if self.agg_stt[0]=="2nd":
                self.agg_stt[0]="5th"
                self.agg_count_inv[0]=0
                return 0
            if self.agg_stt[0]=="5th":
                self.agg_stt[0]="Idle"
                self.agg_qta[0]=0
                self.agg_prz[0]=0.0
                self.agg_ord=[]
                self.agg_count_inv[0]=0
                self.agg_count_flw[0]=0
                self.agg_wait[0]=10
        if self.agg_count_flw[0]==self.agg_num_flw[0] and self.agg_count_inv[0]==self.agg_num_inv[0]:
            if self.agg_stt[0]=="1st":
                self.agg_stt[0]="2nd"
                self.agg_count_inv[0]=0
                self.agg_count_inv[0]
                return 0

            
            
    
