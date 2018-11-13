#!/usr/bin/env python
"""
Pick a random image and tweet it
"""
from __future__ import print_function, unicode_literals
import argparse
import datetime
import os
import random
import sys
from twitter import Twitter, OAuth  # pip install twitter
import yaml                         # pip install pyyaml
import webbrowser

from pprint import pprint


def timestamp():
    """ Print a timestamp and the filename with path """
    print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + " " +
          __file__)


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def load_yaml(filename):
    """Load Twitter credentials from a YAML file"""
    with open(filename) as f:
        data = yaml.safe_load(f)

    keys = data.viewkeys() if sys.version_info.major == 2 else data.keys()
    if not keys >= {
        'oauth_token', 'oauth_token_secret',
        'consumer_key', 'consumer_secret'
    }:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    return data


def random_img_and_text(spec):
    """Find images (non-recursively) in dirname"""
    import glob
    # Get a list of matching images, full path
    matches = glob.glob(spec)

    print("Found", len(matches))

    if not len(matches):
        sys.exit("No files found matching " + spec)

    # Did we get a JSON of filenames and descriptions? e.g.
    # {
    #  "image1.jpg": "Description 1",
    #  "image2.jpg": "Description 2"
    # }

    if len(matches) == 1 and matches[0].endswith(".json"):
        print("JSON")
        import json
        with open(matches[0]) as data_file:
            data = json.load(data_file)
            pprint(data)
            random_image = random.choice(data.keys())
            text = data[random_image]
    else:
        # Pick a random image from the list
        random_image = random.choice(matches)
        text = text_from_filename(random_image)

    print_it("Random image: " + random_image)

    return random_image, text


def text_from_filename(filename):
    """Return 'abc def' from C:\dir\abc_def.jpg"""

    # Get filename without path
    # C:\dir\abc_def.jpg -> abc_def.jpg
    base = os.path.basename(filename)

    # Get name from filename
    name = os.path.splitext(base)[0]

    # Replace underscores with spaces
    name = name.replace("_", " ")
    print_it(name)
    return name


def hashtagify(text):
    """Remove spaces and prepend a hash"""
    return "#" + text.replace(" ", "")


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

    print_it("TWEETING THIS:\n" + string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:
        with open(img, "rb") as imagefile:
            params = {"media[]": imagefile.read(), "status": string}
            result = t.statuses.update_with_media(**params)
            url = ("https://twitter.com/" + result['user']['screen_name'] +
                   "/status/" + result['id_str'])
            print("Tweeted:\n" + url)
            if not args.no_web:
                # 2 = open in a new tab, if possible
                webbrowser.open(url, new=2)


if __name__ == "__main__":

    timestamp()

    parser = argparse.ArgumentParser(
        description="Pick a random image and tweet it",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        default='M:/bin/data/randimgbot.yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument(
        '-i', '--inspec',
        type=unicode,
        default='M:/randomimages/*.jpg',
        help="Input file spec for directory containing images, "
             "or a JSON file of 'image filename': 'description'")
    parser.add_argument(
        '-t', '--template',
        type=unicode,
        default='Random image: {0} #randimgbot {1}',
        help="Tweet template, where {0} will be replaced with a name taken "
             "from the filename, and {1} is a hashtag from the name")
    parser.add_argument(
        '-c', '--chance',
        type=int, default=12,
        help="Denominator for the chance of tweeting this time")
    parser.add_argument(
        '-x', '--test', action='store_true',
        help="Test mode: don't tweet")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    args = parser.parse_args()

    # Do we have a chance of tweeting this time?
    if random.randrange(args.chance) > 0:
        sys.exit("No tweet this time")

    twitter_credentials = load_yaml(args.yaml)

    img, text = random_img_and_text(args.inspec)
    hashtag = hashtagify(text)

    tweet = args.template.format(text, hashtag)
    print_it("Tweet this:\n" + tweet)

    tweet_it(tweet, img, twitter_credentials)

# End of file
