#!/bin/bash

if [[ `git status --porcelain` ]]
then
  git config --local user.email "mgwalker@users.noreply.github.com"
  git config --local user.name "automatic update"
  git commit -m "regular update" -a
  git remote set-url --push origin https://mgwalker:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY
fi