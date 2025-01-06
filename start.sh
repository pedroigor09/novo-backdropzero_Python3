#!/bin/sh
git submodule update --init --recursive
wget <URL_DO_ARQUIVO> -O saved_models/u2net/u2net.pth
exec python my_app.py
