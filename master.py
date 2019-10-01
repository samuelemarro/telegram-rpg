import logging
import sys

import telegram

from action import Action
from character import Character

import session

logger = logging.getLogger(__name__)

def character_status(update, context):
    args = context.args

    if len(args) == 0:
        message = session.state.character_summary
    else:
        character_name = context.args[0]

        character = session.get_character(character_name)

        if character is None:
            message = 'Giocatore non trovato.'
        else:
            message = character.status

    update.message.reply_markdown(message)

# Usare un TextHandler con una stringa iniziale particolare (tipo ?), in modo da poter
# interpretare anche la descrizione. In alternativa puoi usare tutti i caratteri spaziati
# come il contenuto della descrizione.
# Magari "bla bla bla" va interpretato come un unico argomento
# Oppure direttamente interattivo.
# Aggiungere anche supporto template? O magari lavori con un editor
# Telegram supporta gli a capo

def money(update, context):
    #add/remove
    pass

def effect(update, context):
    #add/remove
    #"All" support?
    pass

def victory_points(update, context):
    #add/remove
    pass

def objective(update, context):
    #add/remove
    pass

def reminder(update, context):
    #add/remove
    pass

def approve_action(update, context):
    pass

def approve_objective(update, context):
    pass
    #Idealmente con già l'opzione per dare la nuova carta. Sistema di coda?

def approve_proposal(update, context):
    pass

def pick_action(update, context):
    pass

def add(update, context):
    if len(context.args) == 0:
        update.message.reply_markdown('/add [sotto-comando] [...]')
        return

    sub_command = context.args.pop(0)

    if sub_command == 'character':
        from character import add_character
        add_character(update, context)
    elif sub_command == 'action':
        from action import add_action
        add_action(update, context)
    elif sub_command == 'effect':
        from effect import add_effect
        add_effect(update, context)
    else:
        update.message.reply_markdown('Sotto-comando "{}" non riconosciuto'.format(sub_command))

def _del(update, context):
    if len(context.args) == 0:
        update.message.reply_markdown('/del [sotto-comando] [...]')
        return

    sub_command = context.args.pop(0)

    if sub_command == 'character':
        from character import del_character
        del_character(update, context)
    elif sub_command == 'action':
        from action import del_action
        del_action(update, context)
    else:
        update.message.reply_markdown('Sotto-comando "{}" non riconosciuto'.format(sub_command))
