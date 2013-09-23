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

Estimated response time values are <0.5ms.

* ``make`` to compile.
* ``./measure 8080`` to run and output results.

Results are output to stdout. Measurement data is kept around in case you
want to run additional postprocessing on it.


Example output
--------------

Debian Wheezy with standard packaged apache2-mpm-worker on 8080, and
Varnish 3.0.4 on 6081::

    lkarsten@immer:~/work/httpttfb$ ./measure 8080; ./measure 6081
    localhost:8080 (2013-09-23 14:35:04.326689 on immer)
    --------------------------------------------------

    mean: 264.749μs (stdev 0.000011974) median: 264.279μs
    mean: 268.636μs (stdev 0.000014741) median: 267.876μs
    mean: 254.972μs (stdev 0.000037825) median: 264.978μs
    mean: 272.408μs (stdev 0.000016404) median: 273.568μs
    mean: 272.853μs (stdev 0.000017663) median: 270.496μs

    localhost:6081 (2013-09-23 14:35:16.566675 on immer)
    --------------------------------------------------

    mean: 93.045μs (stdev 0.000001108) median: 92.959μs
    mean: 136.669μs (stdev 0.000039922) median: 147.365μs
    mean: 145.904μs (stdev 0.000005585) median: 144.362μs
    mean: 135.787μs (stdev 0.000012227) median: 136.225μs
    mean: 137.303μs (stdev 0.000008220) median: 138.007μs

    lkarsten@immer:~/work/httpttfb$

