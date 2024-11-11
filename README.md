# randimgbot

[![Test](https://github.com/hugovk/randimgbot/actions/workflows/test.yml/badge.svg)](https://github.com/hugovk/randimgbot/actions/workflows/test.yml)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

Pick a random image and toot it.

## Example

Randimgbot powers **[@FlagFacts@botsin.space on Mastodon](https://mas.to/@FlagFacts)**.

## Set up Mastodon

Create an account at:

https://botsin.space/auth/sign_up

Follow https://gist.github.com/aparrish/661fca5ce7b4882a8c6823db12d42d26 to create a
client ID, client secret, and access token, and store in YAML file. See
`data/randimgbot_example.yaml`.

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run it

Call something like:

```bash
python randimgbot.py -y path/to/randimgbot.yaml -i path/to/dir/full/of/images/*.jpg -t "Random thing: {0} #randomthing {1}"
```

Where `{0}` will be replaced with a name taken from the filename, and `{1}` is a hashtag
from the name. Either or both can be omitted.

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

By default it will only toot randomly 1/12 times. Change this denominator with
`--chance`.

Check full options with:

```bash
python randimgbot.py -h
```
