#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  dnsparse.py
#  Parse a dig-style DNS output.
#
#  Copyright 2020 Edward Wang <edward.c.wang@compdigitec.com>

import re
from typing import Dict, List, TypeVar

_T = TypeVar('_T')

def add_lists(a: List[_T], b: List[_T]) -> List[_T]:  # pylint: disable=invalid-name
    """Helper method: join two lists together while type checking."""
    assert isinstance(a, List)
    assert isinstance(b, List)
    return a + b

class DNSParser:
    """
    Parse a dig-style DNS output.
    """
    def __init__(self, dig_input: str) -> None:
        # Entries look like this:
        # www.mozilla.org.	3	IN	CNAME	www.mozilla.org.cdn.cloudflare.net.
        # www.mozilla.org.cdn.cloudflare.net. 243	IN A	104.18.164.34

        # Create buckets to hold parsed info.
        a_dict: Dict[str, List[str]] = {}
        cname_dict: Dict[str, str] = {}

        # Separate A and CNAMEs.
        for line_raw in dig_input.split("\n"):
            line: str = line_raw.strip()

            # Replace consecutive spaces and tabs
            line = re.sub(r'\s+', "\t", line)

            if line.startswith(";"):
                # Comments begin with ;
                continue

            if len(line) == 0:  # pylint: disable=len-as-condition
                # Empty lines
                continue

            # Break down the line
            line_components = line.split("\t")
            domain = line_components[0]
            ttl: int = int(line_components[1])  # pylint: disable=unused-variable
            # IN
            record_type: str = line_components[3]
            dest: str = line_components[4]
            if record_type == "A":
                if domain not in a_dict:
                    a_dict[domain] = []
                a_dict[domain].append(dest)
            elif record_type == "CNAME":
                if domain in cname_dict:
                    raise ValueError(f"CNAME for {domain} already exists?")
                else:
                    cname_dict[domain] = dest
            else:
                raise NotImplementedError(f"Record type {record_type} not supported")

        self.a_dict = a_dict
        self.cname_dict = cname_dict

    def query(self, domain: str) -> List[str]:
        """
        Query IP addresses for a given domain name.
        """
        # Add trailing '.' for DNS
        if not domain.endswith('.'):
            domain = domain + '.'

        if domain in self.cname_dict:  # pylint: disable=no-else-return
            return self.query(self.cname_dict[domain])
        elif domain in self.a_dict:
            return self.a_dict[domain]
        else:
            raise ValueError(f"No records for domain {domain}")

    def query_single(self, domain: str) -> str:
        """
        Convenient function to return a single entry for a domain name.
        """
        return self.query(domain)[0]

    def dump(self) -> Dict[str, List[str]]:
        """
        Dump all known entries.
        """
        output: Dict[str, List[str]] = {}
        for domain in list(self.cname_dict.keys()) + list(self.a_dict.keys()):
            output[domain[0:-1]] = self.query(domain) # strip '.'
        return output
