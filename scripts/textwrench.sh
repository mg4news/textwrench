#!/bin/bash

# Forward all arguments literally to Python
# "$@" ensures each argument is passed exactly as typed
python3 textwrench.py "$@"
