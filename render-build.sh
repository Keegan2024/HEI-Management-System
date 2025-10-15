#!/bin/bash
pip install gunicorn==21.2.0
gunicorn app:app
