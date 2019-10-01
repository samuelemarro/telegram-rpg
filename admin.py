import logging

import session

logger = logging.getLogger(__name__)

def stop(update, context):
    logger.info('Stopping server...')
    update.message.reply_markdown('Chiudendo il server.')

    session.updater.stop()

    logger.info('Done!')

#kick