from .dataSource.trackseries import save_series
from .utils.config import username, password, image_path, cron_string, timezone
from .utils.logger import logger

from croniter import croniter
from datetime import datetime
import time


def main():
    logger.info("Starting TrackSeriesSaver app")
    iter = croniter(cron_string, datetime.now(tz=timezone))
    next_run = iter.get_next(datetime)
    while True:
        now = datetime.now(tz=timezone)
        time_remaining = (next_run - now).total_seconds()
        if time_remaining <= 0:
            # If the scheduled time has passed, update immediately
            save_series(username, password, image_path)
            iter = croniter(cron_string, datetime.now(tz=timezone))
            next_run = iter.get_next(datetime)
        else:
            # If there is time remaining until the scheduled time, sleep for that duration
            logger.info(f"Application sleeping until {next_run.strftime('%H:%M %Z on the %d.%m')}")
            time.sleep(time_remaining)


if __name__ == "__main__":
    main()
