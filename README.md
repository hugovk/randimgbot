randimgbot
==========

Pick a random image and tweet it.

Set up
------

Create and authorise an app with (read and) write access at:

https://dev.twitter.com/apps/new

Store credentials in YAML file. See data/randimgbot_example.yaml

Install dependencies:

    pip install twitter pyyaml

Run it
------

Call something like:

    randimgbot.py -y path/to/randimgbot.yaml -i path/to/dir/full/of/images/*.jpg -t "Random thing: {0} #randomthing"
