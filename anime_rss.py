#!/usr/bin/env python
"""
    Downloads torrent files from RSS feeds
"""

from os.path import expanduser
import urllib.request
import argparse
import feedparser as fp
import yaml

PARSER = argparse.ArgumentParser(description='Downloads files from RSS feeds')
PARSER.add_argument('-c', '--config', help='Configuration file location',
                    required=False)
PARSER.add_argument('-d', '--download', help='Download directory',
                    required=False)
PARSER.add_argument('-r', '--rss', help='RSS Feed',
                    required=False)
ARGS = vars(PARSER.parse_args())

if ARGS['config'] is not None:
    CONFIG_FILE = ARGS['config']

if ARGS['download'] is not None:
    DOWNLOAD_DIR = ARGS['download']

if ARGS['rss'] is not None:
    RSS_URL = ARGS['rss']


def get_conf():
    """
        Returns a list of titles from config file
    """
    with open(CONFIG_FILE, 'r') as config:
        cfg = yaml.load(config)
        return cfg


HOME = expanduser("~")
CONFIG_FILE = HOME + "/.config/anime_rss/anime_rss.cfg"
DOWNLOAD_DIR = HOME + "/torrents/"
YAML_CFG = get_conf()
TITLE = YAML_CFG["title"]
QUALITY = YAML_CFG["quality"]
SUBBER = YAML_CFG["subber"]
RSS_URL = YAML_CFG["url"]

def check_title(x):
    title = x.get('title')

    if not title:
        return False

    if ARGS['rss'] is not None:
        return all([
            any(str(sub) in title for sub in SUBBER),
            any(str(qul) in title for qul in QUALITY)
        ])


    return all([
        any(str(ti) in title for ti in TITLE),
        any(str(sub) in title for sub in SUBBER),
        any(str(qul) in title for qul in QUALITY)
    ])

for url in RSS_URL:
    feed = fp.parse(url)
    for post in [x for x in feed.entries if check_title(x)]:
        urllib.request.urlretrieve(post.link,
                                    DOWNLOAD_DIR +
                                    post.title +
                                    ".torrent")
        print(post.title + ": " + post.link)
