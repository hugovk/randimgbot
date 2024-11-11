#!/usr/bin/env python
"""
Pick a random image and post it
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import random
import sys
import webbrowser
from pprint import pprint

import yaml  # pip install pyyaml
from mastodon import Mastodon  # pip install Mastodon.py


def timestamp():
    """Print a timestamp and the filename with path"""
    print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + " " + __file__)


def load_yaml(filename):
    """Load credentials from a YAML file"""
    with open(filename) as f:
        data = yaml.safe_load(f)

    if not data.keys() >= {
        "mastodon_client_id",
        "mastodon_client_secret",
        "mastodon_access_token",
    }:
        sys.exit(f"Mastodon credentials missing from YAML: {filename}")

    return data


def random_img_and_text(spec: str) -> tuple[str, str]:
    """Find images (non-recursively) in dirname"""
    import glob

    # Get a list of matching images, full path
    matches = glob.glob(os.path.expanduser(spec))

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
        with open(matches[0]) as data_file:
            data = json.load(data_file)
            pprint(data)
            random_image = random.choice(list(data))
            text = data[random_image]
    else:
        # Pick a random image from the list
        random_image = random.choice(matches)
        text = text_from_filename(random_image)

    print("Random image: " + random_image)

    return random_image, text


def text_from_filename(filename: str) -> str:
    r"""Return 'abc def' from C:\dir\abc_def.jpg"""

    # Get filename without path
    # C:\dir\abc_def.jpg -> abc_def.jpg
    base = os.path.basename(filename)

    # Get name from filename
    name = os.path.splitext(base)[0]

    # Replace underscores with spaces
    name = name.replace("_", " ")
    print(name)
    return name


def hashtagify(text: str) -> str:
    """Remove spaces and prepend a hash"""
    return "#" + text.replace(" ", "")


def toot_it(
    status: str,
    image_path: str,
    credentials: dict[str, str],
    *,
    test: bool = False,
    no_web: bool = False,
    alt_text: str = None,
) -> None:
    """Toot string with an image"""
    if len(status) <= 0:
        return

    # Create and authorise an app with (read and) write access following:
    # https://gist.github.com/aparrish/661fca5ce7b4882a8c6823db12d42d26
    # Store credentials in YAML file
    api = Mastodon(
        credentials["mastodon_client_id"],
        credentials["mastodon_client_secret"],
        credentials["mastodon_access_token"],
        api_base_url="https://botsin.space",
    )

    print("TOOTING THIS:\n", status)

    if test:
        print("(Test mode, not actually tooting)")
        return

    media_ids = []
    if image_path:
        print("Upload image")

        media = api.media_post(media_file=image_path, description=alt_text)
        media_ids.append(media["id"])

    # No geolocation on Mastodon
    # https://github.com/mastodon/mastodon/issues/8340
    # lat, long = closest_point_to_pluto.closest_point_to_pluto()

    toot = api.status_post(status, media_ids=media_ids, visibility="public")

    url = toot["url"]
    print("Tooted:\n" + url)
    if not no_web:
        webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


if __name__ == "__main__":
    timestamp()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pick a random image and toot it",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-y",
        "--yaml",
        default="M:/bin/data/randimgbot.yaml",
        help="YAML file location containing Mastodon keys and secrets",
    )
    parser.add_argument(
        "-i",
        "--inspec",
        default="M:/randomimages/*.jpg",
        help="Input file spec for directory containing images, "
        "or a JSON file of 'image filename': 'description'",
    )
    parser.add_argument(
        "-t",
        "--template",
        default="Random image: {0} #randimgbot {1}",
        help="Tweet template, where {0} will be replaced with a name taken "
        "from the filename, and {1} is a hashtag from the name",
    )
    parser.add_argument(
        "-a",
        "--alt",
        help="Alt text template, where {0} will be replaced with a name taken "
        "from the filename (Mastodon only)",
    )
    parser.add_argument(
        "-c",
        "--chance",
        type=int,
        default=12,
        help="Denominator for the chance of tooting this time",
    )
    parser.add_argument(
        "-x", "--test", action="store_true", help="Test mode: don't toot"
    )
    parser.add_argument(
        "-nw",
        "--no-web",
        action="store_true",
        help="Don't open a web browser to show the tooted toot",
    )
    args = parser.parse_args()

    # Do we have a chance of posting this time?
    if random.randrange(args.chance) > 0:
        print("No post this time")
        sys.exit()

    credentials = load_yaml(args.yaml)

    image_path, text = random_img_and_text(args.inspec)
    hashtag = hashtagify(text)

    status = args.template.format(text, hashtag)
    alt = args.alt.format(text) if args.alt else None
    print("Post this:\n" + status)
    toot_it(
        status,
        image_path,
        credentials,
        test=args.test,
        no_web=args.no_web,
        alt_text=alt,
    )


if __name__ == "__main__":
    main()
