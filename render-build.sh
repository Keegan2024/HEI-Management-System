#!/bin/bash
apt-get update
apt-get install -y meson ninja-build
pip install --upgrade pip
pip install -r requirements.txt
