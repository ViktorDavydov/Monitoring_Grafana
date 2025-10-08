#!/usr/bin/env python3
"""Simple script to run the load generator."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cmd.load.main import main

if __name__ == '__main__':
    print("Starting Load Generator...")
    print("Using only standard Python libraries")
    main()
