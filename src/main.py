#Sistema Economico ad Agenti#
import os
import random
import datetime
import math
import matplotlib.pyplot as plt

from Titolo import *
from Market import *
from Agente import *
from Event_generator import *

agenti=[]
titolo=Titolo(0,"null")
market=Market("null")
sch=[]
retG=[]
bigG=[]
topG=[]
invG=[]
flwG=[]
evG=Event_generator()

               

def crea_agenti(num_top, num_big, num_ret):
    
    for a in range(num_top-3):
        ag=Agente(('t'+str(a)),'top',int(random.uniform(1000000, 10000000))*10000,random.uniform(1, 10),market,1)
        ag.add_ttl(titolo)
        agenti.append(ag)
    for a in range(num_big-10):
        ag=Agente(('b'+str(a)),'big',int(random.uniform(20000, 400000))*10000,random.uniform(1, 10),market,1)
        ag.set_event(evG)
        ag.add_ttl(titolo)
        agenti.append(ag)
    for a in range(num_ret):
        ag=Agente(('r'+str(a)),'retail',int(random.uniform(1000, 10000))*10000,random.uniform(1, 10),market,1)
        ag.add_ttl(titolo)
        agenti.append(ag)


def initialization(conf_file):
    
    f=open(conf_file,'r')
    c=f.readlines()
    
    titolo.set_id_ttl(c[2][3:-1])
    titolo.set_value(int(c[3][6:]))
    evG.set_inst(int(c[4][5:]))
    print c[4][6:]
    market.add_ttl(titolo)
    market.set_id_mrk(c[6][3:-1])
    num_top=int(c[8][4:])
    num_big=int(c[9][4:])
    num_ret=int(c[10][7:])
    sch.append(int(c[12][5:]))
    sch.append(int(c[13][4:]))
    evG.iniztialization()
    crea_agenti(num_top, num_big, num_ret)
    f.close()

    
def stat_mkr(agenti):
    tot_liq=0
    mRet=0
    countR=0
    mTop=0
    countT=0
    mBig=0
    countB=0
    inv=0
    countI=0
    flw=0
    countF=0
    for a in agenti:
        tot_liq+=a.get_lqd()
        if a.typ_agn=="retail":
            mRet+=a.get_lqd()
            countR+=1
        if a.typ_agn=="top":
            mTop+=a.get_lqd()
            countT+=1
        if a.typ_agn=="big":
            mBig+=a.get_lqd()
            countB+=1
        if a.agn_str==7 and a.agg_type=="Inv":
            inv+=a.get_lqd()
            countI+=1
        if a.agn_str==7 and a.agg_type=="Flw":
            flw+=a.get_lqd()
            countF+=1
    invG.append(float(inv/countI)/10000)
    flwG.append(float(flw/countF)/10000)
    topG.append(float(mTop/countT)/10000)
    bigG.append(float(mBig/countB)/10000)
    retG.append(float(mRet/countR)/10000)
    print "Media Top "+str(int(mTop/countT)/10000)
    print "Media Big "+str((mBig/countB)/10000)
    print "Media Retail "+str((mRet/countR)/10000)


def show_grp(dtaT):

    plt.figure(1)
    plt.subplot(711)
    plt.title("Andamento titolo: MBPS")
    plt.plot(dtaT, color='black')
    
    plt.subplot(713)
    plt.title("Media patrimonio Retail")
    plt.plot(retG, color='green')#, 'b-',bigG,'g-')#,topG,'r-')

    plt.subplot(715)
    plt.title("Media patrimonio Big")
    plt.plot(bigG,color='blue')

    plt.subplot(717)
    plt.title("Media patrimonio Top")
    plt.plot(topG,color='red')
    plt.show()

    plt.figure(2)
    plt.subplot(311)
    plt.title("Aggiotaggio: media patrimonio Inv")
    plt.plot(invG, color='black')
    
    plt.subplot(313)
    plt.title("Aggiotaggio: media patrimonio Flw")
    plt.plot(flwG, color='blue')

    plt.show()
    
    
    

def exe():
    ricchezza=[]
    tmp=0.0
    print "Inizio computazione"
    dtaT=[]
    for a in agenti:
        print a.to_string()
    #CICLO su giorni da simulare
    for i in range(sch[0]):
        print "### Day "+str(i+1)+" ###"
        
        #TO DO: genera eventi (del giorno) influenza il titolo ad una determinata iterazione
        print "APERTURA: "
        #for t in market.titoli:
        print "titolo: "+titolo.get_id_ttl()+" valore: 0."+str(titolo.get_value())
        #CICLO su iterazioni giornaliere da eseguire
        for j in range(sch[1]):
            for a in agenti:
                tmp+=float(a.liquidita)/10000
            ricchezza.append(tmp)
            tmp=0.0
            print "Iterazione: "+str(j+1)
            #market.ltl_update()
            for a in agenti:
                a.update_str()
            stat_mkr(agenti)
            market.update()
            for a in agenti:
                a.update_value()
            #market.update_evnt(titolo, evG.get_event())
            #print ''
            #for a in agenti:
            #    print a.to_string()
            #print ''
            evG.next_event()
            print "####Day "+str(i+1)+" Iterazione "+str(j+1)+ " Terminato####"
            print "UPDATE MARKET "+str(titolo.get_value())
            dtaT.append(titolo.get_value())
    print "CHIUSURA: "
    for t in market.titoli:
        print "titolo: "+t.get_id_ttl()+" valore: 0."+str(t.get_value())

    print "ricchezza"
    print ricchezza
    print "Andamento Titolo: "
    print dtaT
    print "Andamento Retail: "
    print retG
    print "Andamento Big: "
    print bigG
    print "Andamento Top: "
    print topG
    show_grp(dtaT)





initialization(os.path.join(os.path.dirname(__file__), '..', 'config', 'conf.txt'))
exe()




