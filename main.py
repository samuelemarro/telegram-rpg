from telegram.ext import Updater
from telegram.ext import ConversationHandler
import logging
import os
import click
from pathlib import Path
import json

import session

from game import GameState
from handler_initialization import initialize_handlers

logger = logging.getLogger(__name__)

def hello(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Oh!')
    update.message.reply_markdown(
        'Hello {}'.format(update.message.from_user.first_name))


# TODO:
# pending_messages
# Applicazione automatica premi
# Backup
# Opzione di attivare/disattivare funzionalità?
# Spese/guadagni ogni turno? Magari attaccandolo al sistema di status?
# Oppure un sistema separato di guadagni/spese

def start_server(telegram_token):
    updater = Updater(telegram_token, use_context=True)
    logger.info('Created updater.')

    session.updater = updater

    for handler in session.handlers:
        updater.dispatcher.add_handler(handler)

    logger.info('Beginning polling.')
    updater.start_polling()
    while True:
        pass
    updater.idle()

def get_input(prompt, acceptable_values=None, accept_callback=None):
    os.system('cls')
    if acceptable_values is None and accept_callback is None:
        print(prompt)
        return input()
    else:
        while True:
            print(prompt)
            if acceptable_values is not None:
                print('[{}]'.format(', '.join(acceptable_values)))

            answer = input()

            if acceptable_values is not None and answer not in acceptable_values:
                print('Answer is not among accepted values.')
                continue

            if accept_callback is not None:
                output = accept_callback(answer)

                if output is None:
                    print('Answer rejected.')
                else:
                    return output
            return answer


@click.group()
def main():
    pass

class Action:
    def __init__(self, name, description, uses):
        self.name = name
        self.description = description
        self.uses = uses


@main.command()
@click.argument('player_token', type=str)
@click.argument('gm_token', type=str)
@click.argument('state_file_path', type=click.Path(file_okay=True, dir_okay=False))
@click.option('--name', type=str, default='Senza nome')
@click.option('--token-path', type=click.Path(exists=True, file_okay=True, dir_okay=False), default='telegram-token.txt')
def start(player_token, gm_token, state_file_path, name, token_path):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    if Path(state_file_path).exists():
        with open(state_file_path, 'r') as f:
            game_state = json.load(f)

        logger.info('Loaded existing state.')
    else:
        game_state = GameState(name)
        logger.info('Created new state.')

    session.state = game_state
    session.player_token = player_token
    session.gm_token = gm_token
    session.state_file_path = state_file_path

    initialize_handlers()

    with open(token_path, 'r') as f:
        telegram_token = f.read()

    start_server(telegram_token)


if __name__ == '__main__':
    main()