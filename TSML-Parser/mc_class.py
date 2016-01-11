from tsml_error import TSMLerror
from string_conversions import events_to_str, transitions_and_observers_to_str, merge_with


class McClass:
    def __init__(self, name, basic_block):
        if not name:
            raise TSMLerror('A Class must have a name')

        if basic_block is None:
            raise TSMLerror('A Class must have a BasicBlockBody')

        self.name = name
        self.identifier = None
        self.states = basic_block.states
        self.events = basic_block.events
        self.transitions = basic_block.transitions
        self.observers = basic_block.observers

    def __str__(self):
        res = 'class ' + self.name + '\n'

        basic_block_res = 'state '

        if isinstance(self.states[0], list):
            for state in self.states:
                basic_block_res += merge_with(state, '&') + ', '
            basic_block_res = basic_block_res.strip(', ')
        else:
            basic_block_res += ', '.join(self.states)

        basic_block_res += ';\n' + events_to_str(self.events) + '\n'
        basic_block_res += transitions_and_observers_to_str(self.transitions, self.observers)

        for line in str(basic_block_res).split('\n'):
            res += '\t' + line + '\n'

        res += 'end\n'

        return res
