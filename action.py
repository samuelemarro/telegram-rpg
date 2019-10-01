import logging

import session

logger = logging.getLogger(__name__)

class Action:
    def __init__(self, name, description, conditions=None, uses=-1):
        self.name = name
        self.conditions = conditions
        self.description = description
        self.uses = uses

    def __str__(self):
        representation = '*{}*'.format(self.name)

        if self.uses == 0 or self.uses > 1:
            representation += ' ({} usi)'.format(self.uses)
        elif self.uses == 1:
            representation += ' (1 uso)'

        if self.description is not None:
            representation += '\n' + self.description

        if self.conditions is not None and self.conditions != "":
            representation += '\nCondizioni: {}\n'.format(self.conditions)

        return representation


def add_action(update, context):
    args = context.args

    if len(args) == 0:
        update.message.reply_text('/add action [personaggio] |[nome]|[usi]|[descrizione]|[condizioni]')
        return
    else:
        character_name = args.pop(0)

        if character_name not in session.state.character_names:
            update.message.reply_markdown('Il personaggio "{}" non esiste.'.format(character_name))
            return


    text = ' '.join(args)
    action_args = text.split('|')

    # Il primo argomento va ignorato
    action_args.pop(0)

    if len(action_args) < 2 or len(action_args) > 4:
        update.message.reply_markdown('Numero errato di argomenti azione ([2-4], ne hai {}).'.format(len(action_args)))
        return

    name = action_args[0]

    try:
        uses = int(action_args[1])
    except ValueError:
        update.message.reply_markdown('"{}" non è un valore valido.'.format(action_args[1]))
        return

    if len(action_args) >= 3:
        description = action_args[2]
    else:
        description = None

    if len(action_args) == 4:
        conditions = action_args[3]
    else:
        conditions = None

    action = Action(name, description, conditions=conditions, uses=uses)

    character = next(x for x in session.state.characters if x.name == character_name)

    character.actions.append(action)
    character.pending_messages.append('Hai ricevuto una nuova azione:\n{}'.format(action))

    logger.info('Added to character {} the action\n{}'.format(character_name, action))
    update.message.reply_markdown('Aggiunta al personaggio {} l\'azione\n{}'.format(character_name, action))

def del_action(update, context):
    args = context.args

    if len(args) == 0:
        update.message.reply_text('/del action [personaggio] |[azione]')
        return

    character_name = args.pop(0)

    character = session.get_character(character_name)

    if character is None:
        update.message.reply_markdown('Il personaggio "{}" non esiste.'.format(character_name))
        return

    text = ' '.join(args)
    action_args = text.split('|')

    if len(action_args) != 2:
        update.message.reply_markdown('Usa |[azione] per indicare il nome dell\'azione.')
        return

    name = action_args[1]

    action = character.get_action(name)

    if action is None:
        update.message.reply_markdown('Il personaggio "{}" non ha l\'azione "{}".'.format(character_name, name))
        return

    character.actions.remove(action)
    logger.info('Deleted action "{}" from character "{}"'.format(name, character_name))

    update.message.reply_markdown('Rimosso l\'azione "{}" dal personaggio "{}"'.format(name, character_name))
