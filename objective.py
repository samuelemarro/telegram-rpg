class Objective:
    def __init__(self, description, victory_points=0, money=0, other_prizes=None):
        self.description = description
        self.victory_points = victory_points
        self.money = money
        self.other_prizes = other_prizes

    def __str__(self):
        representation = '{}\nPremi:'.format(self.description)

        prizes = []
        if self.victory_points != 0:
            prizes.append('{} PV'.format(self.victory_points))
        if self.money != 0:
            prizes.append('{}k franchi'.format(self.money))
        if self.other_prizes is not None:
            prizes.append(self.other_prizes)

        representation += ', '.join(prizes)

        return representation