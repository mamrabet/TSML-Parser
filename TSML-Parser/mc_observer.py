class McObserver:
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __str__(self):
        return self.name + ': ' + self.body
