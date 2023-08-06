import os
import sys
import time
import logging
import datetime
import traceback
import argparse

from better_social_notifications.helper.data import read, write
from better_social_notifications.notification.notify import Notification
from better_social_notifications.youtube.uploads import YouTubeChannels
from better_social_notifications.youtube.auth import APIKeys

"""
TODO
1. Add comments for
"""

logger = logging.getLogger("BSN")


def run():
    sys.excepthook = exception_handler

    parser = setup_args()
    args = parser.parse_args()

    if os.path.exists(args.folder):
        print()
        root_dir = args.folder
    else:
        logger.critical(f"{args.folder} is not a valid path!")
        exit(1)

    os.makedirs(f"{root_dir}/logs/", exist_ok=True)

    secrets = read(f"{root_dir}/data/secrets.json")

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s %(name)s:%(funcName)s:%(lineno)s - %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
        handlers=[
            logging.FileHandler(
                f"{root_dir}/logs/BSN-{datetime.datetime.now()}.log"),
            logging.StreamHandler(),
        ],
    )

    file = f"{root_dir}/data/youtube/uploads.json"

    notification = Notification(secrets["notifications"])

    notification.create(starting_message=True).send()

    keys = APIKeys(secrets["yt_api_keys"])

    while True:
        channels = YouTubeChannels(read(file), keys)

        if len(channels.uploads) > 0:
            notification.create(youtube_upload=channels.uploads).send()
        if len(channels.livestreams) > 0:
            notification.create(youtube_livestream=channels.livestreams).send()
        if len(channels.shorts) > 0:
            notification.create(youtube_short=channels.shorts).send()

        write(file, channels.channel_file_repr)

        logger.info("Sleeping for 10 seconds...")
        time.sleep(10)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', '--folder', help='Full path to the folder to store data files and log files')

    return parser


def exception_handler(type, value, tb):
    logging.error("Uncaught exception: {0}".format(str(value)))
    logging.error("".join(traceback.format_exception(type, value, tb)))


if __name__ == "__main__":
    run()
