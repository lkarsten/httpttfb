httpttfb
========

httpttfb - measure time to first byte. (ttfb)

Run a series of connect+HTTP requests against a HTTP server. Measure how long
it takes to return the first byte.

License: MIT
Author: Lasse Karstensen <lkarsten@varnish-software.com>, September 2013.

Usage
-----

Run this against a web server on your local machine. Network latency will
screw up any serious measurements attempts.
Estimated response time values are are <0.5ms.

* run make to compile.
* ./measure localhost 8080

Results are output to stdout.

