import logging

from telegram.ext import CommandHandler, Handler

import session

logger = logging.getLogger(__name__)

def login(update, context):
    args = context.args

    telegram_id = update.effective_user.id

    if telegram_id == session.gm_telegram_id:
        update.message.reply_markdown('Sei già autenticato come GM.')
        return
    if telegram_id in [x.telegram_id for x in session.users]:
        update.message.reply_markdown('Sei già autenticato come giocatore.')
        return
    
    if len(args) == 0:
        update.message.reply_text('/login [token-giocatore]' \
        ' [nome-personaggio] o /login [token-gm] per fare il login.')
        return

    if args[0] == session.player_token:
        # Autenticazione giocatore
        if len(args) == 1:
            update.message.reply_text('/login [token-giocatore] [nome-personaggio]')
            return

        character_name = args[1]

        if character_name in [x.character.name for x in session.users]:
            other_user = [x.name for x in session.users if x.character.name == character_name][0]
            update.message.reply_markdown('Questo personaggio è già in uso da {}.'.format(other_user))
            return

        character = session.get_character(character_name)

        if character is None:
            update.message.reply_markdown('Questo personaggio non esiste.')
            return

        username = update.message.from_user.first_name + ' ' + update.message.from_user.last_name

        logger.info('Authenticated player {} (ID: {})'.format(username, telegram_id))
        user = User(telegram_id, username, character)
        session.users.append(user)
        
        update.message.reply_markdown('Autenticato come giocatore. Benvenuto/a, {}!'.format(character.name))
    elif args[0] == session.gm_token:
        # Autenticazione GM
        logger.info('Authenticated GM (ID: {})'.format(telegram_id))
        session.gm_telegram_id = telegram_id
        update.message.reply_markdown('Autenticato come GM. Benvenuto/a, master!')
    else:
        update.message.reply_markdown('Token errato.')

class User:
    def __init__(self, telegram_id, name, character):
        self.telegram_id = telegram_id
        self.name = name
        self.character = character

    @property
    def status(self):
        return '*{}*\n{}'.format(self.name, self.character.status)


class UserFilter(Handler):
    def __init__(self, user_type, handler):
        super().__init__(handler.callback,
            pass_update_queue=handler.pass_update_queue,
            pass_job_queue=handler.pass_job_queue,
            pass_user_data=handler.pass_user_data,
            pass_chat_data=handler.pass_chat_data)
        self.handler = handler
        self.user_type = user_type

    def check_update(self, update):
        telegram_id = update.effective_user.id

        if self.user_type == 'gm':
            if telegram_id == session.gm_telegram_id:
                logger.debug('Confirmed GM.')
                return self.handler.check_update(update)
        elif self.user_type == 'player':
            if telegram_id in session.get_user_ids():
                logger.debug('Confirmed player.')
                return self.handler.check_update(update)
        else:
            return self.handler.check_update(update)

    def handle_update(self, update, dispatcher, check_result, context=None):
        return self.handler.handle_update(update, dispatcher, check_result, context)

    def collect_additional_context(self, context, update, dispatcher, check_result):
        return self.handler.collect_additional_context(context, update, dispatcher, check_result)

    def collect_optional_args(self, dispatcher, update=None, check_result=None):
        return self.handler.collect_optional_args(dispatcher, update, check_result)

