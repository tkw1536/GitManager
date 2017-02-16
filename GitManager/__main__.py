#!/usr/bin/env python

import sys
from GitManager import main

if __name__ == '__main__':
    code = main.main(sys.argv)
    sys.exit(code)
