from tsml_error import TSMLerror
from collections import defaultdict
from string_conversions import events_to_str, synchronizations_and_observers_to_str


class McBlock:
    def __init__(self, name, internal_block):
        if not name:
            raise TSMLerror('A Block must have a name')

        if internal_block is None:
            raise TSMLerror('A Block must contain an InternalBlockBody')

        self.name = name
        self.identifier = None
        self.blocks = internal_block.blocks
        self.class_instances = internal_block.class_instances
        self.events = internal_block.events
        self.synchronizations = internal_block.synchronizations
        self.observers = internal_block.observers

    def __str__(self):
        res = 'block ' + self.name + '\n'

        internal_block_res = ''
        for block in self.blocks:
            internal_block_res += str(block)

        if isinstance(self.class_instances, list):
            class_instances = defaultdict(list)
            for class_object in self.class_instances:
                class_instances[class_object.name].append(class_object.identifier)
        else:
            class_instances = self.class_instances

        for class_name in class_instances:
                internal_block_res += class_name + ' ' + ', '.join(class_instances[class_name]) + ';\n'

        internal_block_res += events_to_str(self.events) + '\n'
        internal_block_res += synchronizations_and_observers_to_str(self.synchronizations, self.observers)

        for line in str(internal_block_res).split('\n'):
            res += '\t' + line + '\n'

        res += 'end\n'

        return res
