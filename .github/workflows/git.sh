#!/bin/bash

if [[ `git status --porcelain` ]]
then
  echo "committing and pushing changes"
  git config --local user.email "mgwalker@users.noreply.github.com"
  git config --local user.name "automatic update"
  git commit -m "regular update" -a
  git push "https://mgwalker:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY" HEAD:master
else
  echo "no changes detected; skipping"
fi