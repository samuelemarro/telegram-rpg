from telegram.ext import CommandHandler
import logging
logger = logging.getLogger(__name__)

state = None
player_token = None
gm_token = None
state_file_path = None
updater = None
gm_telegram_id = None
users = []
handlers = []

def get_user_ids():
    return [x.telegram_id for x in users]

def get_active_character_names():
    return [x.character.name for x in users]

def get_character(character_name):
    matching_characters = [x for x in state.characters if x.name == character_name]

    if len(matching_characters) == 0:
        return None
    else:
        return matching_characters[0]