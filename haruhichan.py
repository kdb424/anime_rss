#!/usr/bin/env python
"""
    Downloads titles from haruhichan.com automatically from the RSS feed
"""

from os.path import expanduser
import urllib.request
import argparse
import feedparser as fp
import yaml

RSS_URL = "http://haruhichan.com/feed/feed.php?mode=rss"

FEED = fp.parse(RSS_URL)

HOME = expanduser("~")
CONFIG_FILE = HOME + "/.config/haruhichan.cfg"
DOWNLOAD_DIR = HOME + "/Downloads/"


PARSER = argparse.ArgumentParser(description='Downloads files from Haruhichan RSS')
PARSER.add_argument('-c', '--config', help='Configuration file location',
                    required=False)
PARSER.add_argument('-d', '--download', help='Download directory',
                    required=False)
ARGS = vars(PARSER.parse_args())

if ARGS['config'] is not None:
    CONFIG_FILE = ARGS['config']

if ARGS['download'] is not None:
    DOWNLOAD_DIR = ARGS['download']


def get_conf():
    """
        Returns a list of titles from config file
    """
    with open(CONFIG_FILE, 'r') as config:
        cfg = yaml.load(config)
        return cfg


YAML_CFG = get_conf()
TITLE = YAML_CFG["title"]
QUALITY = YAML_CFG["quality"]
SUBBER = YAML_CFG["subber"]
for post in FEED.entries:
    for title in TITLE:
        if str(title) in post.title:
            for sub in SUBBER:
                if str(sub) in post.title:
                    for qul in QUALITY:
                        if str(qul) in post.title:
                            urllib.request.urlretrieve(post.link,
                                                       DOWNLOAD_DIR +
                                                       post.title +
                                                       ".torrent")
                            print(post.title + ": " + post.link)
