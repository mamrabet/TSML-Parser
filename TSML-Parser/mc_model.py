from post_process import post_process


class McModel:
    def __init__(self, classes, blocks):
        self.blocks = blocks
        self.classes = classes
        post_process(self)

    def __str__(self):
        res = ''

        for mcClass in self.classes:
            res += str(mcClass) + '\n'

        for mcBlock in self.blocks:
            res += str(mcBlock) + '\n'

        return res.strip('\n')