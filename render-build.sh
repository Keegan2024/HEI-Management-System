#!/bin/bash
apt-get update
apt-get install -y meson ninja-build
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn==21.2.0  # Ensure gunicorn is installed
