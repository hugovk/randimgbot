#!/bin/bash
set -e

python3 randimgbot.py --yaml ~/bin/data/flagfacts.yaml --no-web  -i "~/github/flagfactsflags/flags/*.png" -t "{0}" --chance 6 --mastodon
python3 randimgbot.py --yaml ~/bin/data/flagfacts.yaml --no-web  -i "~/github/flagfactsflags/flags/*.png" -t "{0}" --chance 6 --twitter
