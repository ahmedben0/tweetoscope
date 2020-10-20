import logger

logger = logger.get_logger('my-node', broker_list='localhost:9092', debug=True)  # the source string (here 'my-node') helps to identify
                                                                                 # in the logger terminal the source that emitted a log message.

logger.debug("Are you feeling that burning smell?")  # DEBUG level are only display if the logger debug argument is set to true
logger.info("Hey, do you know the latest?")          # INFO level for normal messages
logger.warning("You shouldn't do that.")             # WARNING
logger.error("What you ask me is just nonsense!")    # recoverable ERROR
logger.critical("Houston, we have a problem.")       # CRITICAL errors abort the application
