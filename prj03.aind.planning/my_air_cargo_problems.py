from aimacode.logic import PropKB
from aimacode.planning import Action
from aimacode.search import (
    Node, Problem,
)
from aimacode.utils import expr
from lp_utils import (
    FluentState, encode_state, decode_state,
)
from my_planning_graph import PlanningGraph

from functools import lru_cache


class AirCargoProblem(Problem):
    def __init__(self, cargos, planes, airports, initial: FluentState, goal: list):
        """

        :param cargos: list of str
            cargos in the problem
        :param planes: list of str
            planes in the problem
        :param airports: list of str
            airports in the problem
        :param initial: FluentState object
            positive and negative literal fluents (as expr) describing initial state
        :param goal: list of expr
            literal fluents required for goal test
        """
        self.state_map = initial.pos + initial.neg
        self.initial_state_TF = encode_state(initial, self.state_map)
        Problem.__init__(self, self.initial_state_TF, goal=goal)
        self.cargos = cargos
        self.planes = planes
        self.airports = airports
        self.actions_list = self.get_actions()

    def get_actions(self):
        """
        This method creates concrete actions (no variables) for all actions in the problem
        domain action schema and turns them into complete Action objects as defined in the
        aimacode.planning module. It is computationally expensive to call this method directly;
        however, it is called in the constructor and the results cached in the `actions_list` property.

        Returns:
        ----------
        list<Action>
            list of Action objects
        """

        def load_actions():
            """Create all concrete Load actions and return a list

            :return: list of Action objects
            """
            loads = []
            # the Actions format is (expression, [ [precondition_pos],[precondition_neg] ], [[effect_add],[effect_rem]]
            # for each (cargo, plane, airport)
            # create all possible load actions
            for cargo in self.cargos:
                for plane in self.planes:
                    for airport in self.airports:
                        precondition_positive = [
                            expr("At({}, {})".format(cargo, airport)),
                            expr("At({}, {})".format(plane, airport)), ]
                        precondition_negative = []
                        effect_add = [expr("In({}, {})".format(cargo, plane))]
                        effect_rem = [expr("At({}, {})".format(cargo, airport))]
                        load = Action(expr("Load({}, {}, {})".format(cargo, plane, airport)),
                                      [precondition_positive, precondition_negative],
                                      [effect_add, effect_rem])
                        loads.append(load)
            return loads

        def unload_actions():
            """Create all concrete Unload actions and return a list

            :return: list of Action objects
            """
            unloads = []
            # for each (cargo, plane, airport)
            # create all possible unload actions
            for cargo in self.cargos:
                for plane in self.planes:
                    for airport in self.airports:
                        precondition_positive = [
                            expr("In({}, {})".format(cargo, plane)),
                            expr("At({}, {})".format(plane, airport)),
                        ]
                        precondition_negative = []
                        effect_add = [expr("At({}, {})".format(cargo, airport))]
                        effect_rem = [expr("In({}, {})".format(cargo, plane))]
                        unload = Action(expr("Unload({}, {}, {})".format(cargo, plane, airport)),
                                        [precondition_positive, precondition_negative],
                                        [effect_add, effect_rem])
                        unloads.append(unload)
            return unloads

        def fly_actions():
            """Create all concrete Fly actions and return a list

            :return: list of Action objects
            """
            flights = []
            for fr in self.airports:
                for to in self.airports:
                    if fr != to:
                        for p in self.planes:
                            precondition_positive = [expr("At({}, {})".format(p, fr)), ]
                            precondition_neg = []
                            effect_add = [expr("At({}, {})".format(p, to))]
                            effect_rem = [expr("At({}, {})".format(p, fr))]
                            fly = Action(expr("Fly({}, {}, {})".format(p, fr, to)),
                                         [precondition_positive, precondition_neg],
                                         [effect_add, effect_rem])
                            flights.append(fly)
            return flights

        return load_actions() + unload_actions() + fly_actions()

    def load_knowledgeBase(self, state: str, onlyPositive=False) -> PropKB:
        """
        Return the knowledge base
        :param state: 
        :param onlyPositive:
        :return: 
        """
        kb = PropKB()
        if onlyPositive:
            kb.tell(decode_state(state, self.state_map).pos_sentence())
        else:
            kb.tell(decode_state(state, self.state_map).sentence())
        return kb

    def actions(self, state: str) -> list:
        """ Return the actions that can be executed in the given state.

        :param state: str
            state represented as T/F string of mapped fluents (state variables)
            e.g. 'FTTTFF'
        :return: list of Action objects
        """
        kb = self.load_knowledgeBase(state)  # load the truthfulness of each of the predicates
        possible_actions = []
        for action in self.actions_list:
            if action.check_precond(kb, action.args):
                possible_actions.append(action)
        return possible_actions

    def result(self, state: str, action: Action):
        """ Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        :param state: state entering node
        :param action: Action applied
        :return: resulting stateTF after action
        """
        kb = self.load_knowledgeBase(state)  # read the kb
        action(kb, action.args)  # apply the action
        new_state = FluentState(kb.clauses, [])
        return encode_state(new_state, self.state_map)

    def goal_test(self, state: str) -> bool:
        """ Test the state to see if goal is reached

        :param state: str representing state
        :return: bool
        """
        kb = self.load_knowledgeBase(state, onlyPositive=True)
        for clause in self.goal:
            if clause not in kb.clauses:
                return False
        return True

    def h_1(self, node: Node):
        # note that this is not a true heuristic
        h_const = 1
        return h_const

    @lru_cache(maxsize=8192)
    def h_pg_levelsum(self, node: Node):
        """This heuristic uses a planning graph representation of the problem
        state space to estimate the sum of all actions that must be carried
        out from the current state in order to satisfy each individual goal
        condition.
        """
        # requires implemented PlanningGraph class
        pg = PlanningGraph(self, node.state)
        pg_levelsum = pg.h_levelsum()
        return pg_levelsum

    @lru_cache(maxsize=8192)
    def h_ignore_preconditions(self, node: Node):
        """This heuristic estimates the minimum number of actions that must be
        carried out from the current state in order to satisfy all of the goal
        conditions by ignoring the preconditions required for an action to be
        executed.
        """
        kb = self.load_knowledgeBase(node.state, onlyPositive=True)
        goals = set(self.goal) - set(kb.clauses)
        count = 0
        while goals:
            for action in self.actions_list:
                env = clone_kb(kb)
                action.act_relaxed(env, action.args)
                goals_left = goals - set(env.clauses)
                if len(goals_left) < len(goals): # we are moving to the write direction
                    count +=1
                    goals = goals_left
                    kb = env
        return count


def air_cargo_p1() -> AirCargoProblem:
    cargos = ['C1', 'C2']
    planes = ['P1', 'P2']
    airports = ['JFK', 'SFO']
    pos = [
        expr('At(C1, SFO)'),
        expr('At(C2, JFK)'),
        expr('At(P1, SFO)'),
        expr('At(P2, JFK)'),
    ]
    neg = [
        expr('At(C1, JFK)'),
        expr('At(C2, SFO)'),
        expr('At(P1, JFK)'),
        expr('At(P2, SFO)'),
        expr('In(C1, P1)'),
        expr('In(C1, P2)'),
        expr('In(C2, P1)'),
        expr('In(C2, P2)'),
    ]
    init = FluentState(pos, neg)
    goal = [expr('At(C1, JFK)'),
            expr('At(C2, SFO)'),
            ]
    return AirCargoProblem(cargos, planes, airports, init, goal)


def air_cargo_p2() -> AirCargoProblem:
    cargos = ['C1', 'C2', 'C3']
    planes = ['P1', 'P2', 'P3']
    airports = ['JFK', 'SFO', 'ATL']
    pos = [
        expr('At(C1, SFO)'),
        expr('At(C2, JFK)'),
        expr('At(C3, ATL)'),
        expr('At(P1, SFO)'),
        expr('At(P2, JFK)'),
        expr('At(P3, ATL)'),
    ]
    neg = [
        expr('At(C1, ATL)'),
        expr('At(C1, JFK)'),
        expr('At(C2, ATL)'),
        expr('At(C2, SFO)'),
        expr('At(C3, SFO)'),
        expr('At(C3, JFK)'),
        expr('At(P1, ATL)'),
        expr('At(P1, JFK)'),
        expr('At(P2, ATL)'),
        expr('At(P2, SFO)'),
        expr('At(P3, JFK)'),
        expr('At(P3, SFO)'),
        expr('In(C1, P1)'),
        expr('In(C1, P2)'),
        expr('In(C1, P3)'),
        expr('In(C2, P1)'),
        expr('In(C2, P2)'),
        expr('In(C2, P3)'),
        expr('In(C3, P1)'),
        expr('In(C3, P2)'),
        expr('In(C3, P3)'),
    ]
    init = FluentState(pos, neg)
    goal = [
        expr('At(C1, JFK)'),
        expr('At(C2, SFO)'),
        expr('At(C3, SFO)')
    ]

    return AirCargoProblem(cargos, planes, airports, init, goal)


def air_cargo_p3() -> AirCargoProblem:
    cargos = ['C1', 'C2', 'C3', 'C4']
    planes = ['P1', 'P2']
    airports = ['JFK', 'SFO', 'ATL', 'ORD']
    pos = [
        expr('At(C1, SFO)'),
        expr('At(C2, JFK)'),
        expr('At(C3, ATL)'),
        expr('At(C4, ORD)'),
        expr('At(P1, SFO)'),
        expr('At(P2, JFK)'),
    ]
    cargo_at_airport = {
        expr('At({}, {})'.format(c, a)) for c in cargos for a in airports
    }
    cargo_in_plane = {
        expr('In({}, {})'.format(c, p)) for p in planes for c in cargos
    }
    plane_at_airport = {
        expr('At({}, {})'.format(p, a)) for p in planes for a in airports
    }
    # everything else but the positive predicates belong in the negative list
    # set1.union(set2) == set1 | set2
    neg = list((cargo_at_airport | plane_at_airport | cargo_in_plane) - set(pos))

    init = FluentState(pos, neg)
    goal = [
        expr('At(C1, JFK)'),
        expr('At(C3, JFK)'),
        expr('At(C2, SFO)'),
        expr('At(C4, SFO)'),
    ]
    return AirCargoProblem(cargos, planes, airports, init, goal)


def clone_kb(kb: PropKB) -> PropKB:
    """
    Instead of rebuilding a knowledge base we just clone the clauses
    :param kb: 
    :return: 
    """
    clone = PropKB()
    clone.clauses = kb.clauses.copy()
    return clone
