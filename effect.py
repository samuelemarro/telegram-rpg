import logging

import session

logger = logging.getLogger(__name__)

class Effect:
    def __init__(self, name, description=None, active=True, duration=-1, money_per_turn=0):
        self.name = name
        self.description = description
        self.active = active
        self.duration = duration
        self.money_per_turn = money_per_turn

    def __str__(self):
        representation = '*{}*'.format(self.name)

        extra_info = []

        extra_info.append('Attivo' if self.active else 'Passivo')
        
        if self.duration != -1:
            extra_info.append('{} turni'.format(self.duration))

        if self.money_per_turn != 0:
            extra_info.append('{}k/turno'.format(self.money_per_turn))

        representation += ' (' + ', '.join(extra_info) + ')'

        if self.description is not None:
            representation += '\n' + self.description 

        return representation


def add_effect(update, context):
    args = context.args

    if len(args) == 0:
        update.message.reply_text('/add effect [personaggio] |[nome]|[descrizione]|[attivo]|[durata]|[denaro-per-turno]')
        return

    character_name = args.pop(0)

    character = session.get_character(character_name)

    if character is None:
        update.message.reply_markdown('Il personaggio "{}" non esiste.'.format(character_name))
        return

    text = ' '.join(args)
    effect_args = text.split('|')

    effect_args.pop(0)

    if len(effect_args) < 1 or len(effect_args) > 5:
        update.message.reply_text('Numero errato di argomenti effetto ([1-5], ne hai {}).'.format(len(effect_args)))
        return

    name = effect_args[0]

    if name in [x.name for x in character.effects]:
        update.message.reply_markdown('Il personaggio "{}" ha già l\'effetto "{}".'.format(character_name, name))
        return

    if len(effect_args) >= 2:
        description = effect_args[1]
    else:
        description = None

    
    if len(effect_args) >= 3:
        active = effect_args[2]

        positive_answers = ['yes', 'si', 'y']
        negative_answers = ['no', 'n']

        if active in positive_answers:
            active = True
        elif active in negative_answers:
            active = False
        else:
            update.message.reply_markdown('"{}" non è un valore booleano valido.'.format(effect_args[2]))
            return
    else:
        active = True

    if len(effect_args) >= 4:
        try:
            duration = int(effect_args[3])
        except ValueError:
            update.message.reply_markdown('"{}" non è un valore valido.'.format(effect_args[2]))
            return
    else:
        duration = -1

    if len(effect_args) == 5:
        try:
            money_per_turn = int(effect_args[4])
        except ValueError:
            update.message.reply_markdown('"{}" non è un valore valido.'.format(effect_args[2]))
            return
    else:
        money_per_turn = 0

    effect = Effect(name, description=description, active=active, duration=duration, money_per_turn=money_per_turn)

    character.effects.append(effect)

    character.pending_messages.append('Hai un nuovo effetto:\n{}'.format(effect))

    logger.info('Added to character {} the effect\n{}'.format(character_name, effect))
    update.message.reply_markdown('Aggiunto al personaggio {} l\'effetto\n{}'.format(character_name, effect))
    