import logging

import session

logger = logging.getLogger(__name__)

class Character:
    def __init__(self, name, money=0, victory_points=0, effects=[], actions=[], objectives=[]):
        self.name = name
        self.money = money
        self.victory_points = victory_points
        self.effects = effects
        self.actions = actions
        self.objectives = objectives
        self.pending_messages = []

    @property
    def status(self):
        status = '*{}*\n\n'.format(self.name)
        
        status += '{}k franchi, {} PV\n\n'.format(self.money, self.victory_points)

        status += 'Effetti:\n\n'

        status += '\n\n'.join([str(x) for x in self.effects])

        status += 'Obiettivi:\n\n'

        status += '\n\n'.join([str(x) for x in self.objectives])

        status += 'Actions:\n\n'

        status += '\n\n'.join([str(x) for x in self.actions])

        return status

    def get_action(self, action_name):
        actions = [x for x in self.actions if x.name == action_name]

        if len(actions) == 0:
            return None
        else:
            return actions[0]

def add_character(update, context):
    args = context.args

    if len(args) == 0:
        update.message.reply_text('/add character [personaggio] [denaro iniziale]')
        return

    character_name = args[0]

    if character_name in session.state.character_names:
        update.message.reply_markdown('Il personaggio "{}" esiste già'.format(character_name))
        return

    if len(args) == 2:
        try:
            money = int(args[1])
        except ValueError:
            update.message.reply_markdown('"{}" non è un valore valido.'.format(args[1]))
            return
    else:
        money = 0

    character = Character(character_name, money=money)

    session.state.characters.append(character)

    logger.info('Added character {}'.format(character_name))
    update.message.reply_markdown('Aggiunto personaggio "{}"'.format(character_name))

def del_character(update, context):
    args = context.args

    if len(args) == 0:
        update.message.reply_text('/del character [personaggio]')
        return

    character_name = args[0]

    if character_name in session.get_active_character_names():
        username = [x.name for x in session.users if x.character.name == character_name][0]
        update.message.reply_markdown('Il personaggio {} è al momento usato da {}'.format(character_name, username))
        return

    character = session.get_character(character_name)

    if character is None:
        update.message.reply_markdown('Il personaggio {} non esiste'.format(character_name))
        return

    session.state.characters.remove(character)

    logger.info('Removed character "{}".'.format(character_name))
    update.message.reply_markdown('Il personaggio {} è stato rimosso'.format(character_name))

def use_action(update, context):
    pass

def claim_objective(update, context):
    pass

def propose_action(update, context):
    # Possibilità di rimuoverla?
    pass

def make_offer(update, context):
    pass

def status(update, context):
    pass