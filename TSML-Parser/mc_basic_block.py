from tsml_error import TSMLerror
from string_conversions import events_to_str, transitions_and_observers_to_str


class McBasicBlock:
    def __init__(self, states, events, transitions, observers):
        if not states:
            raise TSMLerror('a StateClause cannot be empty')
        if not events:
            raise TSMLerror('an EventClause cannot be empty')
        if not transitions:
            raise TSMLerror('a TransitionClause cannot be empty')

        self.states = states
        self.events = events
        self.transitions = transitions
        self.observers = observers
