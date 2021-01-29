#!/bin/bash

if [ -z "$1" ]; then echo "Usage: $0 PROJECT_NAME"; exit 1; fi
PROJECT=$1
ORIG="https://github.com/tango-controls"
DEST="https://gitlab.com/tango-controls"
BRANCH="moved-to-gitlab"

set -x
git clone $ORIG/$PROJECT
cd $PROJECT
git checkout --orphan $BRANCH
git rm -rf .
echo "## $PROJECT moved to $DEST/$PROJECT" > README.md
git add .
git commit -m "Move to $DEST/$PROJECT"
git push origin $BRANCH
