#!/bin/bash
pip3 install -r requirements.txt -t lib/
zip -r lupseat.zip * -x "__pycache__/*" -x ".git/*" -x "tests/*" -x "*.txt" -x "*.csv" -x "*.zip"
