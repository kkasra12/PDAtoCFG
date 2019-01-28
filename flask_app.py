from flask import Flask,render_template,request
from pda import state,pda
from utils import Normalize, MakeCFG
from pprint import pprint

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("getData.html")

@app.route("/toCFG")
def todfa():
    states_json = eval(request.values['states'])
    states = {}
    for s in states_json:
        isInitial,isFinal=False,False
        if s.get("isInitial"):
            isInitial=True
        if s.get("isFinal"):
            isFinal=True
        states.update({s['id']:state(s['label'],isFinal=isFinal,isInitial=isInitial)})
    transitions_json = eval(request.values['transitions'])
    for t in transitions_json:
        states[t['from']].connect(states[t['to']],t['label'],t['pop'],t['push'])
    machine=pda()
    for s in states.values():
        machine.add_state(s)
    #return (str(machine).replace("\n","<br>"))
    normal_machine=Normalize(machine)
    grammer = MakeCFG(normal_machine)

    states_json = []
    transitions_json = []
    transition_id = 0
    print(machine)
    for s in normal_machine.states:
        new_state = {"id":s.name,"label":s.name}
        if s.isFinal:
            new_state.update({"isFinal":1})
        if s.isInitial:
            new_state.update({"isInitial":1})
        states_json.append(new_state)
        tmp = s.get_neighbours()
        for t in tmp:
            for next_s in tmp[t]:
                new_edge = {"id":str(transition_id),"from":s.name,"to":next_s,"arrows":"to"}
                tmp0 = []
                for i in [0,1,2]:
                    if t[i]=="":
                        tmp0.append(chr(955))
                    else:
                        tmp0.append(str(t[i]))
                new_edge.update({"label":tmp0[0]+", "+tmp0[1]+" --> "+tmp0[2]})
                transitions_json.append(new_edge)
                transition_id+=1
    good_grammer = ""
    for i in grammer:
        good_grammer+="<br>"+str(i)+" ---> "+"|".join(["".join(j) for j in grammer[i]])
    return render_template("show_dfa.html",states_json=states_json,transitions_json=transitions_json,grammer=good_grammer)

if __name__=="__main__":
    app.run(debug=True)
