#!/usr/bin/env python3
"""Simple script to run the demo server."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cmd.app.main import main

if __name__ == '__main__':
    print("Starting Demo HTTP Server...")
    print("Using only standard Python libraries + prometheus-client")
    main()



