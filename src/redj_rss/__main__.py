from __future__ import annotations

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from pathlib import Path
import random
import sys

import msgpack

## Appends the src/ dir at ../ to Python's path
#  Allows accessing files in i.e. ../.serialize
sys.path.append(".")

import json

from typing import Union

from loguru import logger as log
from main import app

if __name__ == "__main__":
    app()
