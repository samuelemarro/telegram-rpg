from telegram.ext import CommandHandler
from authentication import UserFilter

import session

def initialize_handlers():
    # Login
    from authentication import login
    login_handler = CommandHandler('login', login)
    session.handlers.append(login_handler)

    # Stop (GM only)
    from admin import stop
    stop_handler = CommandHandler('stop', stop)
    stop_handler = UserFilter('gm', stop_handler)
    session.handlers.append(stop_handler)

    # Global character status (GM only)
    from master import character_status
    character_status_handler = CommandHandler('status', character_status)
    character_status_handler = UserFilter('gm', character_status_handler)
    session.handlers.append(character_status_handler)

    # Add (GM only)
    from master import add
    add_handler = CommandHandler('add', add)
    add_handler = UserFilter('gm', add_handler)
    session.handlers.append(add_handler)

    # Del (GM only)
    from master import _del
    del_handler = CommandHandler('del', _del)
    del_handler = UserFilter('gm', del_handler)
    session.handlers.append(del_handler)

    # My status (Player only)

