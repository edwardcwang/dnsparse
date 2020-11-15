#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  dns2hosts.py
#  Convert a dig-style DNS output into a hosts file.
#
#  Copyright 2020 Edward Wang <edward.c.wang@compdigitec.com>

import sys
from typing import Dict, List

from dnsparse import DNSParser

def main(args: List[str]) -> int:
    try:
        with open(args[1], 'r') as f:
            input_contents = str(f.read())
    except IndexError:
        print(f"Usage: {args[0]} INPUT_DIG_STYLE_DNS", file=sys.stderr)
        return 1
    parser = DNSParser(input_contents)
    for key, value in parser.dump().items():
        print(f"{value[0]}\t{key}")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
