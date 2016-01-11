from string_conversions import events_to_str, synchronizations_and_observers_to_str


class McInternalBlock:
    def __init__(self, blocks, class_instances, events, synchronizations, observers):
        self.blocks = blocks
        self.class_instances = class_instances
        self.events = events
        self.synchronizations = synchronizations
        self.observers = observers