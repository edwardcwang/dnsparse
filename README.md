Simple script to generate a hosts file from `dig`-style DNS dumps, and
associated parsing library.

To run:
```shell
dig @1.1.1.1 \
www.google.com \
www.bing.com \
github.com \
www.quora.com > dig.txt
./dns2hosts.py dig.txt > hosts
```

Development: please run `./test.py` to ensure that the tests pass.
