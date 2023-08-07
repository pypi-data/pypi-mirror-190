from IPython.display import display, Image, Math, Latex, HTML

counter = 0

def parse_fa(description, type="dfa"):
    global counter
    allow_partial = False
    lines = []
    for line in description.split('\n'):
        line = line.strip()
        if line == '' or line[0] == '#':
            continue
        lines.append(line)
    line = lines.pop(0)
    if line.startswith('name:'):
        _,name = line.split()
        line = lines.pop(0)
    else:
        name = f"{type}{counter}"
        counter += 1
    if line.startswith('states:'):
        states = set(line[7:].split())
    else:
        raise Exception("Expected states line..")
    if not states:
        raise Exception("Empty states list .. !?")
    line = lines.pop(0)
    if line.startswith('input_symbols:'):
        input_symbols = set(line[14:].split())
    else:
        raise Exception("Expected input_symbols line..")
    if not input_symbols:
        raise Exception("Empty input_symbols set .. !?")
    trans = lines.pop(0)
    if not trans == "transitions:":
        raise Exception(f"Expected transitions header line: {trans}")

    tlines = []
    initial_state_line = ""
    for _ in range(len(lines)):
        line = lines.pop(0)
        if 'initial_state:' in line:
            initial_state_line = line
            break
        tlines.append(line)
    if initial_state_line == "":
        raise Exception("Expected initial_state line..")

    delta = dict()
    for line in tlines:
        if type == "dfa":
            state, d = __parse_dfa_line(line)
        else:
            state, d = __parse_nfa_line(line, input_symbols)
        delta[state] = d

    _,initial_state = initial_state_line.split()

    line = lines.pop(0)
    if line.startswith('final_states:'):
        final_states = set(line[13:].split())
    else:
        raise Exception("Expected final_states line..")
    if type == 'dfa':
        return name, states, input_symbols, delta, initial_state, final_states, allow_partial
    else:
        return name, states, input_symbols, delta, initial_state, final_states

def __parse_dfa_line(line):
    items = line.replace(':', ' ').split()
    if len(items)%2 == 0:
        raise Exception(f"Invalid transitions line: {line}")
    state = items.pop(0)
    d = dict()
    for i in range(0, len(items), 2):
        symbol,kstate = items[i:i+2]
        d[symbol] = kstate
    return state, d

def __parse_nfa_line(line, input_symbols):
    d = dict()
    for s in input_symbols:
        d[s] = set()

    i = line.find(':')
    if i == -1:
        raise Exception(f"Invalid transitions line: {line}")
    state = line[:i].strip()
    for item in line[i+1:].split(","):
        item = item.strip()
        if item == "":
            break
        if not ":" in item:
            raise Exception(f"Invalid transitions line: {line}")
        k,v = item.split(":")
        if k == "epsilon":
            k = ''
        d[k] =  set(v.split())

    return state, d

def _auto_name(self, type):
    global counter
    name = f"{type}{counter}"
    self.__dict__['name'] = name
    counter += 1
    return name

