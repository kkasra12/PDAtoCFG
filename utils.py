from pda import state,pda

def normalize_FinalStates(machine):
    FinalStates = machine.get_finalStates()
    StackAlphabet = machine.get_StackAlphabet()
    virtual_FinalState = state("virtual_FinalState",isFinal=True)
    to_add=[("",i,"") for i in StackAlphabet]
    for s in FinalStates:
        for trans in to_add:
            if trans in s.neighbours:
                s.neighbours[trans].append(virtual_FinalState)
            else:
                s.neighbours.update({trans:[virtual_FinalState]})
        s.isFinal=False
    machine.add_state(virtual_FinalState)
    return machine
def normalize_transitions(machine):
    #check if all transitions pop sth
    ans_machine = pda()
    #e-->w ==> i==wi (for i in stack_alphabet U {$})(e===epsilon)(w is a string)($ is stacks initial variable)
    StackAlphabet = machine.get_StackAlphabet()
    for s in machine.states:
        for t in s.neighbours:
            if len(t[1])>1 or len(t[0])>1:
                raise Exception("fook u:/\nget lost from bitchment!!")
            if t[1]=="":
                for i in StackAlphabet:
                    s.connect(s.neighbours[t],t[0],i,t[2]+i)
                    s.neighbours.pop(t)
    unused_char=find_unused_char(StackAlphabet)
    for s in machine.states:
        for t in s.neighbours:
            if len(t[2])==1:
                '''
                D(q0,a,X)=(q1,A)
                #D(q0,a,X)=(qt,BA) ['B' is unused_char]
                #D(qt,E,B)=(q1,E)  [E is epsilon]
                '''
                state_tmp = find_unused_state(machine)
                next_states = s.neighbours[t]
                machine.add_state(state_tmp)
                s.neighbours.pop(t)
                s.connect(state_tmp,t[0],t[1],unused_char+t[2])
                for next_state in next_states:
                    state_tmp.connect(next_state,"",unused_char,"")
            elif len(t[2])>2:
                '''
                t:   0 1       2
                D(q0,a,X)=(q1,ABCDE)
                #D(q0 ,a,X)=(qt0,DE)                {i=4}
                #D(q0 ,E,D)=(qt0,CD)                {i=3}
                #D(qt0,E,C)=(qt1,BC) [E is epsilon] {i=2}
                #D(qt1,E,B)=(q1 ,AB) [E is epsilon] {i=1}
                '''
                FirstState = s
                alpha = t[0]
                pop=t[1]
                for i in range(len(t[2])-1,0,-1):
                    if i!=1:
                        NextState=find_unused_state(machine)
                    else:
                        NextState=s.neighbours[t][0]
                    machine.add_state(NextState)
                    FirstState.connect(NextState,alpha,pop,t[2][i-1:i+1])
                    FirstState=NextState
                    alpha=""
                    pop=t[2][i-1]
                s.neighbours.pop(t)
    return machine
def Normalize(machine):
    return normalize_transitions(normalize_FinalStates(machine))

def MakeCFG(machine):
    grammer = {}
    for s in machine.states:
        for t in s.neighbours:
            if len(t[2])==0:
                state_name = "("+str(s.name)+"-"+t[1]+"-"+s.neighbours[t][0].name+")"
                if not state_name in grammer:
                    if t[0]=="":
                        grammer.update({state_name:[[chr(955)]]})
                    else:
                        grammer.update({state_name:[[t[0]]]})
                else:
                    if t[0]=="":
                        grammer[state_name].append([chr(955)])
                    else:
                        grammer[state_name].append([t[0]])
            elif len(t[2])==2:
                Nstate = s.neighbours[t][0]
                for s0 in machine.states:
                    state_name = "("+str(s.name)+"-"+t[1]+"-"+s0.name+")"
                    if not state_name in grammer:
                        grammer.update({state_name:[]})
                    for s1 in machine.states:
                        grammer[state_name].append([
                                    t[0],
                                    "("+Nstate.name+"-"+t[2][0]+"-"+s1.name+")",
                                    "("+s1.name    +"-"+t[2][1]+"-"+s0.name+")"
                                    ])
            else:
                #print(len(t[2]))
                raise Exception("unbelievable Error!!!")
    #lets sumorize the grammer
    sumorized_grammer = {}
    for i in grammer:
        to_add = []
        for j in grammer[i]:
            if len(j)==1:
                to_add.append(j)
            elif j[1] in grammer and j[2] in grammer:
                to_add.append(j)
            if len(to_add)>0:
                sumorized_grammer.update({i:to_add})
    return sumorized_grammer

def find_unused_char(lst):
    tmp = list(range(65,91 ))
    tmp+= list(range(97,123))
    for i in tmp:
        if not chr(i) in lst:
            return chr(i)
def find_unused_state(machine):
    t=0
    for s in machine.states:
        if s.name=="q"+str(t):
            t+=1
    return state("q"+str(t))

def npda2cfg(machine):
    return MakeCFG(Normalize(machine))

if __name__=="__main__":
        q0 = state("q0",isInitial=True)
        q1 = state("q1")
        q2 = state("q2",isFinal=True)
        q0.connect(q0,"a","z","Az")
        q0.connect(q0,"a","A","A")
        q0.connect(q1,"b","A","")
        q1.connect(q2,"" ,"z","")
        m0 = pda()
        for i in [q0,q1,q2]:#,q3,q4]:
            m0.add_state(i)
        #print(m0.get_StackAlphabet())
        #print("-"*20)
        print(m0)
        grammer=MakeCFG(Normalize(m0))
        good_grammer=""
        for i in grammer:
            good_grammer+="\n"+str(i)+" ---> "+"|".join(["".join(j) for j in grammer[i]])
        print(good_grammer)
        print(grammer)
