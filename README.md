randimgbot
==========

[![Build Status](https://travis-ci.org/hugovk/python-ci-static-analysis.svg?branch=master)](https://travis-ci.org/hugovk/python-ci-static-analysis)
[![Python: 3.4+](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Pick a random image and tweet it.

Example
-------

Randimgbot powers **[@FlagFacts](https://twitter.com/FlagFacts)**.

Set up
------

Create and authorise an app with (read and) write access at:

https://dev.twitter.com/apps/new

Store credentials in YAML file. See `data/randimgbot_example.yaml`.

Install dependencies:

```bash
pip install twitter pyyaml
```

Run it
------

Call something like:

```bash
python randimgbot.py -y path/to/randimgbot.yaml -i path/to/dir/full/of/images/*.jpg -t "Random thing: {0} #randomthing {1}"
```

Where `{0}` will be replaced with a name taken from the filename, and `{1}` is a hashtag from the name. Either or both can be omitted.

Alternatively with a JSON file:

```bash
python randimgbot.py -y path/to/randimgbot.yaml -i data/randimgbot_example.json -t "Random thing: {0} #randomthing {1}"
```

Where the JSON file looks something like data/randimgbot_example.json:

```json
{
  "image1.jpg": "Description 1",
  "image2.jpg": "Description 2\nLine 2"
}
```

By default it will only tweet randomly 1/12 times. Change this denominator with `--chance`.

Check full options with:

```bash
python randimgbot.py -h
```
