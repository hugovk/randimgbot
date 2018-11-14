#!/bin/bash
set -e

cd ~/github/flagfactsflags/
git checkout master
git pull origin master

cd ~/github/nanogenmobot/
./update.sh
./run.sh
