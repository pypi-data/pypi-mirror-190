from automata.fa.nfa import NFA
from .util import parse_fa
#dot = r'c:\Graphviz7.01\bin\dot.exe'

def __nfa_init(self, description=None, *, states=None, input_symbols=None,
                     transitions=None, initial_state=None,
                     final_states=None):
    """Initialize a complete NFA."""
    if description:
        name, states, input_symbols, transitions, initial_state, final_states = parse_fa(description, 'nfa')
        #print(f"name={name}")
        #self.name = name
        self.__dict__['name'] = name
    super(NFA, self).__init__(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
        _lambda_closures=self._compute_lambda_closures(states, transitions)
    )

NFA.__init__ = __nfa_init

