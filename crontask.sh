#!/bin/bash
set -e

cd ~/github/flagfactsflags/
git checkout main
git pull origin main

cd ~/github/randimgbot/
./update.sh
./run.sh
