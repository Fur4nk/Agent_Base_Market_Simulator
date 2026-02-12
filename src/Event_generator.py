import random

class Event_generator:
    #costruttore
    def __init__(self):
        self.instability=0
        self.hystory=[]
        self.future=[]
    #viene impostato il valore di instabilita
    def set_inst(self, inst):
        self.instability=inst

    
    def next_event(self):
        self.future.pop(0)
        
    #genera i futuri 1000 eventi
    def iniztialization(self):
        x=0
        y=0
        for i in range(1000):
            x=random.randint(-10,10)
            
            y=random.uniform(0,100)
            if y<self.instability:
                y=1
            else:
                y=0
            self.future.append(x*y)
    #ritorna il prossimo eveto, in caso la lista di eventi sia vuota ne genera uno al momento
    def update(self):
        y=random.randint(0,100)
        if y>self.instability:
            x=random.randint(-10,10)
            self.hystory.append(x)
            return int(x)
        return -999
    #da in output una lista di numero x eventi
    def oracle(self, x):
        tmp=[]
        for i in range(x):
            tmp.append(int(self.future[i]))
        return tmp
    #restituisce un singolo evento
    def get_event(self):
        if len(self.future)!=0:
            x=self.future.pop(0)
            self.hystory.append(x)
            return int(x)

        return self.update()
    #imposta l'id del titolo a cui il generatore fa riferimento
    def set_id_ttl(self,id_ttl):
        self.id_ttl=id_ttl
