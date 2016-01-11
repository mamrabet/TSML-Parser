from string_conversions import merge_with


class McTransition:
    def __init__(self, event, start, arrival):
        self.event = event
        self.start = start
        self.arrival = arrival

    def __str__(self):
        if isinstance(self.arrival, list):
            start = merge_with(self.start, '&')
            arrival = merge_with(self.arrival, '&')
        else:
            start = self.start
            arrival = self.arrival

        return self.event + ': ' + start + ' -> ' + arrival
