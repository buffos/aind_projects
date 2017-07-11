from aimacode.utils import expr, Expr
from lp_utils import FluentState, encode_state, decode_state , conjunctive_sentence
from aimacode.logic import PropKB

ex1 = expr('At(C1, SFO)')  # type: Expr
print("ex1 is of type: ", type(ex1))
print("it has 3 members. an op '{}' args {} and the hash {}".format(ex1.op, ex1.args, ex1.__hash__()))

# lets see problem 1 definitions
cargos = ['C1', 'C2']
planes = ['P1', 'P2']
airports = ['JFK', 'SFO']

pos = [expr('At(C1, SFO)'),
       expr('At(C2, JFK)'),
       expr('At(P1, SFO)'),
       expr('At(P2, JFK)'),
       ]
neg = [expr('At(C2, SFO)'),
       expr('In(C2, P1)'),
       expr('In(C2, P2)'),
       expr('At(C1, JFK)'),
       expr('In(C1, P1)'),
       expr('In(C1, P2)'),
       expr('At(P1, JFK)'),
       expr('At(P2, SFO)'),
       ]
init = FluentState(pos, neg)
goal = [expr('At(C1, JFK)'),
        expr('At(C2, SFO)'),
        ]

# lets see the FluentState object
# it has 2 main functions
print(init.sentence())
# that will print all predicates as a sentence like
# (At(C1, SFO) & At(C2, JFK) & At(P1, SFO) & At(P2, JFK) & ~At(C2, SFO) & ~In(C2, P1) & ~In(C2, P2) & ~At(C1, JFK)
#    & ~In(C1, P1) & ~In(C1, P2) & ~At(P1, JFK) & ~At(P2, SFO))
# and
print(init.pos_sentence())
# that omits the negation predicates

# initial state of the AirCargoProblem would be
state_map = init.pos + init.neg # all predicates
initial_state_TF = encode_state(init, state_map) # their mapped state (True or False)
print("The initial state of the Air Cargo Problem would be",state_map)
print("The initial_TF state of the Air Cargo Problem would be", initial_state_TF)
# decoding a state requires giving first the truth state of the predicates and then the predicates
# it returns a FluentObject and can extract a sentence with the sentence member function

# it creates a propositional logic statement
# based on the truth or false of the predicate
print(decode_state('FT', ['At(C1, SFO)','At(C2, SFO)']).sentence())


kb = PropKB()
# this simply extracts the sentence to atomic clauses
kb.tell(decode_state('FT', ['At(C1, SFO)','At(C2, SFO)']).sentence())
print(kb.clauses)