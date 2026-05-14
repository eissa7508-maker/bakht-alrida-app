#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# السطر ده هو اللي بيحل مشكلة الـ Status 1
apt-get update && apt-get install -y tesseract-ocr