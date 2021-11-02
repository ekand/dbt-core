
import dbt.logger as logger  # type: ignore # TODO eventually remove dependency on this logger
from dbt.events.history import EVENT_HISTORY
from dbt.events.types import CliEventABC, Event, ShowException


# top-level method for accessing the new eventing system
# this is where all the side effects happen branched by event type
# (i.e. - mutating the event history, printing to stdout, logging
# to files, etc.)
def fire_event(e: Event) -> None:
    EVENT_HISTORY.append(e)
    if isinstance(e, CliEventABC):
        if e.level_tag() == 'test' and not isinstance(e, ShowException):
            # TODO after implmenting #3977 send to new test level
            logger.GLOBAL_LOGGER.debug(logger.timestamped_line(e.cli_msg()))
        elif e.level_tag() == 'test' and isinstance(e, ShowException):
            # TODO after implmenting #3977 send to new test level
            logger.GLOBAL_LOGGER.debug(
                logger.timestamped_line(e.cli_msg()),
                exc_info=e.exc_info,
                stack_info=e.stack_info,
                extra=e.extra
            )
        elif e.level_tag() == 'debug' and not isinstance(e, ShowException):
            logger.GLOBAL_LOGGER.debug(logger.timestamped_line(e.cli_msg()))
        elif e.level_tag() == 'debug' and isinstance(e, ShowException):
            logger.GLOBAL_LOGGER.debug(
                logger.timestamped_line(e.cli_msg()),
                exc_info=e.exc_info,
                stack_info=e.stack_info,
                extra=e.extra
            )
        elif e.level_tag() == 'info' and not isinstance(e, ShowException):
            logger.GLOBAL_LOGGER.info(logger.timestamped_line(e.cli_msg()))
        elif e.level_tag() == 'info' and isinstance(e, ShowException):
            logger.GLOBAL_LOGGER.info(
                logger.timestamped_line(e.cli_msg()),
                exc_info=e.exc_info,
                stack_info=e.stack_info,
                extra=e.extra
            )
        elif e.level_tag() == 'warn' and not isinstance(e, ShowException):
            logger.GLOBAL_LOGGER.warning(logger.timestamped_line(e.cli_msg()))
        elif e.level_tag() == 'warn' and isinstance(e, ShowException):
            logger.GLOBAL_LOGGER.warning(
                logger.timestamped_line(e.cli_msg()),
                exc_info=e.exc_info,
                stack_info=e.stack_info,
                extra=e.extra
            )
        elif e.level_tag() == 'error' and not isinstance(e, ShowException):
            logger.GLOBAL_LOGGER.error(logger.timestamped_line(e.cli_msg()))
        elif e.level_tag() == 'error' and isinstance(e, ShowException):
            logger.GLOBAL_LOGGER.error(
                logger.timestamped_line(e.cli_msg()),
                exc_info=e.exc_info,
                stack_info=e.stack_info,
                extra=e.extra
            )
        else:
            raise AssertionError(
                f"Event type {type(e).__name__} has unhandled level: {e.level_tag()}"
            )