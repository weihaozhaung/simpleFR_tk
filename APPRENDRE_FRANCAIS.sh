#!/bin/bash -l

git pull origin main
conda run python FR_vocab_app.py
git add .
git commit -m "progressing knowledge in mots francais!"
git push -u origin main

sleep 5
