#!/bin/bash
sudo apt-get update
sudo apt-get install -y meson ninja-build
pip install --upgrade pip
pip install -r requirements.txt
