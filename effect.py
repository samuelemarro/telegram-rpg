class Effect:
    def __init__(self, name, description, duration=-1):
        self.name = name
        self.description = description
        self.duration = duration

    def __str__(self):
        if self.duration == -1:
            return '*{}*\n{}'.format(self.name, self.description)
        else:
            return '*{}* ({} turni)\n{}'.format(self.name, self.duration, self.description)