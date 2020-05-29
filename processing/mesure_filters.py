import logging
import config
logger = logging.getLogger("filtering")

def primal_filter(measure):
    hr = measure["hr"]
    # rr = measure["rr"]
    if hr > 120:
        logger.critical("Person is under stress")
        return True
    else:
        logger.info("Person is in mind control")
        return False