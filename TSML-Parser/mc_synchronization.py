from tsml_error import TSMLerror


class McSynchronization:
    def __init__(self, name, event_paths):
        if name:
            if len(event_paths) < 2:
                raise TSMLerror('A MacroEventDefinition must have several EventPaths')

            self.name = name
            self.event_paths = event_paths
        else:
            self.name = None
            self.event_paths = event_paths

    @property
    def event_path(self):
        if self.name is not None:
            raise TSMLerror('A named Synchronization must have several EventPaths')

        return self.event_paths

    def __str__(self):
        if isinstance(self.event_paths, list):
            res = self.name + ': '

            for event_path in self.event_paths:
                res += str(event_path) + ' & '

            return res.strip(' & ')
        else:
            return str(self.event_path)
