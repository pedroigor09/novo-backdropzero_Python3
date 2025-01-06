#!/bin/sh
git submodule update --init --recursive
exec python my_app.py
