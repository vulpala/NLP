states = ('noun', 'verb', 'inf', 'prep')

observations = ('bears', 'fish')

start_probability = {'noun': 0.8, 'verb': 0.1, 'inf':0.0001, 'prep':0.0001}

transition_probability = {
    'noun' : {'noun': 0.0001, 'verb': 0.65, 'inf':0.0001, 'prep':0.30},
    'verb' : {'noun': 0.77, 'verb': 0.0001, 'inf':0.22, 'prep':0.25},
    'inf'  : {'noun': 0.0001, 'verb': 0.75, 'inf':0.0001, 'prep':0.0001},
    'prep' : {'noun': 0.85, 'verb': 0.0001, 'inf':0.0001, 'prep':0.0001}
   }

emission_probability = {
    'noun' : {'bears': 0.02, 'fish': 0.08},
    'verb' : {'bears': 0.02, 'fish': 0.07},
    'inf' : {'bears': 0.0001, 'fish': 0.0001},
    'prep' : {'bears': 0.0001, 'fish': 0.0001},
   }

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
        print("P(" + obs[0] + "=" + y + ") = " + str(V[0][y]))

    print("------------")

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
            #for y1 in states:
                #print("1=" + str(V[t-1][y1]) + " ** 2=" + str(trans_p[y1][y]) + " ** 3="+ str(emit_p[y][obs[t]]) + " = " + str(V[t-1][y1] * trans_p[y1][y] * emit_p[y][obs[t]]))
            V[t][y] = prob
            print("P(" + obs[t] + "=" + y + ") = " + str(V[t][y]))
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(obs) != 1:
        n = t
    print_dptable(V)
    (prob, state) = max((V[n][y], y) for y in states)
    return (prob, path[state])

# Don't study this, it just prints a table of the steps.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    #print("V = ",V)
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)

def example():
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)
print(example())