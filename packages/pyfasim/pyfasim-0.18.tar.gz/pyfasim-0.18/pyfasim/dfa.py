from automata.fa.dfa import DFA
from .util import parse_fa, display, Image, Math, Latex, HTML, __auto_name
#dot = r'c:\Graphviz7.01\bin\dot.exe'

def __dfa_init(self, description=None, *, states=None, input_symbols=None,
                     transitions=None, initial_state=None,
                     final_states=None, allow_partial=False):
    """Initialize a complete DFA."""
    if description:
        name, states, input_symbols, transitions, initial_state, final_states, allow_partial = parse_fa(description, 'dfa')
        #print(f"name={name}")
        #self.name = name
        self.__dict__['name'] = name
    super(DFA, self).__init__(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
        allow_partial=allow_partial
    )
    object.__setattr__(self, '_word_cache', [])
    object.__setattr__(self, '_count_cache', [])

def __diagram(self):
    pd = self.show_diagram()
    if hasattr(self, 'name'):
        name = self.name
    else:
        name = __auto_name(self)
    #pngfile = f"d:/cmfl/code/FA/{name}.png"
    pngfile = f"{name}.png"
    pd.write_png(pngfile)
    #pd.write_png(pngfile, prog=dot)
    display(Image(pngfile))

def __compseq(self, w):
    #print(f"input={w}")
    it = self.read_input_stepwise(w, ignore_rejection=True)
    i = 0
    #s =  r"\mathbf{%s}" % (self.initial_state,)
    s =  r"\mathbf{%s}" % (next(it),)
    Q = []
    while True:
        try:
            q = next(it)
            s += r"\xrightarrow{\;\textbf{%s}\;}\mathbf{%s}" % (w[i],q)
            #r"\xrightarrow{\text{\;%s\;}}%s" % (w[i],q)
            #s += r"\xrightarrow{%s}%s" % (w[i],q)
            Q.append(q)
            i += 1
        except Exception as e:
            print(e)
            break
    #print(f"Q={Q}")
    if Q[-1] in self.final_states:
        print(f"ACCEPTED: {w}")
    else:
        print(f"REJECTED: {w}")
    display(HTML("<br/>"))
    display(Latex(f'${s}$'))

def __words_of_lengths(self, n1, n2=None):
    W = list(self.words_of_length(n1))
    if n2 is None:
        return W
    for n in range(n1+1, n2+1):
        L = list(self.words_of_length(n))
        W.extend(L)
    return W

def __random_words(self, m, n=1):
    words = set()
    if n<1:
        return list()
    for i in range(0, 2**(m+1)):
        w = self.random_word(m)
        words.add(w)
        if len(words) == n:
            break
    return list(words)

def __getitem(self, subscript):
    if isinstance(subscript, slice):
        start, stop, step = subscript.start, subscript.stop, subscript.step
        if step is None:
            step = 1
        if step>0:
            sign=1
        else:
            sign=-1
        words = list()
        for i in range(start, stop+sign, step):
            words.extend(self.words_of_length(i))
    else:
        words = list(self.words_of_length(subscript))
    return words
   
DFA.__init__ = __dfa_init
DFA.diagram = __diagram
DFA.compseq = __compseq
DFA.words_of_lengths = __words_of_lengths
DFA.random_words = __random_words
DFA.__getitem__ = __getitem


