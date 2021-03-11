#!/bin/bash
python3 setup.py bdist_wheel
python3 -m twine upload dist/LupSeat-$(cat VERSION)*
