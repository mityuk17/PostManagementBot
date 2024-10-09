import logging
from schemas import Post, Channel
from texts import logs_texts


logging.basicConfig(
    filename="bot_events.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s:  %(message)s"
)


def post_publication(post_data: Post):
    logging.info(logs_texts.post_publication(post_data))
    

def post_deleted(post_data: Post):
    logging.info(logs_texts.post_deleted(post_data))
    
    
def post_cancelled(post_data: Post):
    logging.info(logs_texts.post_cancelled(post_data))
    

def post_not_found(post_id: int):
    logging.error(logs_texts.post_not_found(post_id))


def channel_added(channel_data: Channel):
    logging.info(logs_texts.channel_added(channel_data))


def channel_removed(channel_data: Channel):
    logging.info(logs_texts.channel_removed(channel_removed))
    
    
def channel_not_found(channel_id: int):
    logging.error(logs_texts.channel_not_found(channel_id))
    

def no_messages_copied(post_data: Post):
    logging.error(logs_texts.no_messages_copied(post_data))