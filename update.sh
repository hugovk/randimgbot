#!/bin/bash
set -e

date

# Install dependencies
python3 -m pip install -r requirements.txt

git checkout main
git pull origin main
