#!/usr/bin/env python
"""
Pick a random image and tweet it
"""
from __future__ import print_function, unicode_literals
import argparse
import os
import random
from twitter import *  # pip install twitter
import urllib
import yaml
import webbrowser


def load_yaml(filename):
    """Load Twitter credentials from a YAML file"""
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {'oauth_token', 'oauth_token_secret',
                              'consumer_key', 'consumer_secret'}:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    return data


def random_img(dirname):
    """Find images (non-recursively) in dirname"""
    import glob
    # Join the directory with a filespec
    spec = os.path.join(dirname, "*.jpg")
    # Get a list of matching images, full path
    matches = glob.glob(spec)
    print("Found", len(matches), "images")
    
    # Pick a random image from the list
    random_image = random.choice(matches)
    print("Random image:", random_image)
    return random_image


def name_from_filename(filename):
    """Return 'abc def' from C:\dir\abc_def.jpg"""

    # Get filename without path
    # C:\dir\abc_def.jpg -> abc_def.jpg
    base = os.path.basename(filename)

    # Get name from filename
    name = os.path.splitext(base)[0]

    # Replace underscores with spaces
    name = name.replace("_", " ")
    print(name)
    return name


def open_url(url):
    """Open URL in a web browser"""
    print(url)
    if not args.no_web:
        webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def tweet_it(string, img, credentials):
    """Tweet string with an image"""
    if len(string) <= 0:
        # TODO error
        return

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file. See data/randimgbot_example.yaml
    t = Twitter(auth=OAuth(credentials['oauth_token'],
                           credentials['oauth_token_secret'],
                           credentials['consumer_key'],
                           credentials['consumer_secret']))

    print("TWEETING THIS:\n", string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:
        with open(img, "rb") as imagefile:
            params = {"media[]": imagefile.read(), "status": string}
            result = t.statuses.update_with_media(**params)
            url = "https://twitter.com/" + result['user']['screen_name'] + "/status/" + result['id_str']
            print("Tweeted:\n" + url)
            if not args.no_web:
                # 2 = open in a new tab, if possible
                webbrowser.open(url, new=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pick a random image and tweet it",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-y', '--yaml',
        default='M:/bin/data/randimgbot.yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument('-d', '--dir', 
        default='M:/randomimages/',
        help="Directory containing images to tweet at random")
    parser.add_argument('-x', '--test', action='store_true',
        help="Test mode: don't tweet")
    parser.add_argument('-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    args = parser.parse_args()

    twitter_credentials = load_yaml(args.yaml)

    img = random_img(args.dir)

    name = name_from_filename(img)
    
    tweet = "Random image: " + name  + " #randimgbot"
    print("Tweet this:\n", tweet)
    
    tweet_it(tweet, img, twitter_credentials)

# End of file
