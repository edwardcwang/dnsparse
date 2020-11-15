#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test.py
#  Unit tests for dnsparse.
#
#  Copyright 2020 Edward Wang <edward.c.wang@compdigitec.com>

from typing import Dict, List
import unittest

from dnsparse import DNSParser

SIMPLE_DIG = """
; This is a comment
www.mozilla.org.	3	IN	CNAME	www.mozilla.org.cdn.cloudflare.net.
www.mozilla.org.cdn.cloudflare.net.	243	IN	A	104.18.164.34
;; This is also a comment
www.videolan.org.	300	IN	A	213.36.253.2
;;;; Another comment
www.quora.com.	86389	IN	CNAME	quora.map.fastly.net.
quora.map.fastly.net.	19	IN	A	151.101.1.2
quora.map.fastly.net.	19	IN	A	151.101.193.2
"""

class DNSParserTest(unittest.TestCase):
    """
    Test parsing dig outputs.
    """
    def test_query(self) -> None:
        """
        Test querying outputs.
        """
        parser = DNSParser(SIMPLE_DIG)
        self.assertEqual(parser.query_single("www.mozilla.org"), "104.18.164.34")
        self.assertEqual(parser.query_single("www.mozilla.org.cdn.cloudflare.net"), "104.18.164.34")
        self.assertEqual(parser.query_single("www.videolan.org"), "213.36.253.2")
        self.assertEqual(parser.query_single("www.quora.com"), "151.101.1.2")

        # Query all
        self.assertEqual(sorted(parser.query("www.quora.com")), sorted(["151.101.1.2", "151.101.193.2"]))

        # Non-existent
        self.assertRaises(ValueError, lambda: parser.query_single("www2.verilog.net"))
        self.assertRaises(ValueError, lambda: parser.query_single("rofl"))

    def test_dump(self) -> None:
        """
        Test dumping all known IPs.
        """
        parser = DNSParser(SIMPLE_DIG)
        expected_outputs: Dict[str, List[str]] = {
            "www.mozilla.org": ["104.18.164.34"],
            "www.mozilla.org.cdn.cloudflare.net": ["104.18.164.34"],
            "www.videolan.org": ["213.36.253.2"],
            "www.quora.com": ["151.101.1.2", "151.101.193.2"],
            "quora.map.fastly.net": ["151.101.1.2", "151.101.193.2"]
        }
        self.assertEqual(parser.dump(), expected_outputs)

if __name__ == '__main__':
    unittest.main()
