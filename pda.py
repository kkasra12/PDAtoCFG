class  state:
    def __init__(self, name, isFinal=False, isInitial=False):
        self.name = name
        self.isFinal = isFinal
        self.isInitial = isInitial
        self.neighbours = {} # {(symbol,pop,push):[state(s)]}
    def connect(self, next_state, symbol, pop, push):
        if type(next_state)!=type(self):
            print(next_state,symbol,pop,push)
            raise Exception("type error!!")
        if type(symbol)!=type("") or type(pop)!=type("") or type(push)!=type(""):
            raise Exception("type error!!256")

        transition_banner = (symbol,pop,push)
        if transition_banner in self.neighbours:
            if next_state in self.neighbours[transition_banner]:
                return
            print("# WARNING: duplicated transition!! ")
            self.neighbours[transition_banner].append(next_state)
        else:
            self.neighbours.update({transition_banner:[next_state]})
        return True
    def get_neighbours(self):
        return {i:[j.name for j in self.neighbours[i]] for i in self.neighbours}
    def all_nextStates(self):
        tmp=[]
        for i in self.neighbours.values():
            for j in i:
                if not j in tmp:
                    tmp.append(j)
        return tmp
    def __str__(self):
        ans = str(self.name)
        tmp=0
        if self.isFinal:
            ans += " (Final)"
            tmp=8
        if self.isInitial:
            ans += " (Initial)"
            tmp=10
        tmp += len(self.name)
        n=self.get_neighbours()
        keys = list(n)
        try:
            for i in keys[:-1]:
                ans += "--"+str(i)+"-->"+str(n[i])+"\n\t"+" "*tmp
            ans += "--"+str(keys[-1])+"-->"+str(n[keys[-1]])
        except:
            pass
        return ans
    def __lt__(self,other):
        if type(other) != type(self):
            raise "type error!!"
        return self.name < other.name
    def __eq__(self,other):
        return type(other)==type(self) and other.name==self.name and self.isFinal==other.isFinal and self.isInitial==other.isInitial
    def copy(self):
        return state(self.name,isInitial=self.isInitial,isFinal=self.isFinal)
class pda:
    def __init__(self):
        self.states = [] #list of state classes
    def find_count(self, state_name):
        '''find the number of state in the states list'''
        return [i.name for i in self.states].find(state_name)
    def add_state_byname(self, state_name):
        if state_name in [i.name for i in self.states]:
            raise "duplicated state name\n\tstates_list:\t"+str(self.states)+"\n\tnew state name\t" + state_name
        self.states.append(state(state_name))
        return True
    def add_state(self,state_toadd):
        if state_toadd not in self.states:
            self.states.append(state_toadd)
    def __str__(self):
        return "states: " + "-".join([i.name for i in self.states]) + "\n\t" + "\n\t".join([str(i) for i in self.states]) + "\n" + "-"*20
    def get_initialStates(self):
        return [i for i in self.states if i.isInitial]
    def get_finalStates(self):
        return [i for i in self.states if i.isFinal]
    def get_alphabet(self):
        alphabet = []
        for i in self.states:
            for j in i.neighbours:
                if j[0] not in alphabet:
                    alphabet.append(j[0])
        return alphabet
    def get_StackAlphabet(self):
        alphabet = []
        for i in self.states:
            for j in i.neighbours:
                if len(j[1])!=0 and j[1] not in alphabet:
                    alphabet.append(j[1])
                if len(j[2])==1:
                    if j[2] not in alphabet:
                        alphabet.append(j[2])
                else:
                    for tmp in j[2]:
                        if tmp not in alphabet:
                            alphabet.append(tmp)

        return alphabet


if __name__ == "__main__":
    q0 = state("q0",isInitial=True)
    q1 = state("q1")
    q2 = state("q2",isFinal=True)
    q3 = state("q3")
    q4 = state("q4")
    q0.connect(q1,"0","a","#")
    q0.connect(q2,"3","b","#")
    q0.connect(q3,"3","b","#")
    q2.connect(q1,"r","y","5")
    q2.connect(q1,"5","y","5")
    print(q0)
    print(q1)
    print(q2)
    '''
    for i in grammer:
        good_grammer+="\n"+str(i)+" ---> "+"|".join(["".join(j) for j in grammer[i]])'''
