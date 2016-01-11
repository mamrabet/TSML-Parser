class McPath:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        if isinstance(self.parent, str):
            return self.parent + '.' + self.name
        else:
            return self.parent.identifier + '.' + self.name