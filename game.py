import session

class GameState:
    def __init__(self, name):
        self.name = name
        self.current_turn = 0
        self.characters = []
        self.reminders = []
        self.turn_state = ''
        self.global_effects = []

    @property
    def character_names(self):
        return [x.name for x in self.characters]

    @property
    def character_summary(self):
        summary = '**{} giocatori**\n\n'.format(len(self.characters))
        for character in self.characters:
            summary += '**{}**:'' {}k franchi, {} PV,' \
            ' {} azioni, {} obiettivi, {} effetti' \
            '\n'.format(character.name,
                        character.money,
                        character.victory_points,
                        len(character.actions),
                        len(character.objectives),
                        len(character.effects))

        return summary