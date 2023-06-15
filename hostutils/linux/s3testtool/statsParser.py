#!/usr/bin/env python
#
# Capture output of S3TestTool.jar runs, then process the data like this:
#
#    ./statsParser.py screenlog.0 [screenlog.1 ...]
#
# .. or remotely:
#
#    ssh test-host cat screenlog.0 screenlog.1 | ./statsParser.py -

import sys
import re
from datetime import datetime
from collections import OrderedDict

# Globals
REGEX = re.compile(
    r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d*) INFO .* OVERALL (\d+) objects, (\d+) bytes, (\d+) errors, AVG \(([\.\d]+) obj, ([\.\d]+) (.)*B\)/s, ([\.\d]+) ms latency')
ipREGX, thrREGX, sizeREGX = (None, None, None)  # Will define only if used
headerPrinted = False


def parse(fd, cache=None, appendix=None):
    """ Parses the outputs of S3TestTool.jar, and converts into CSV.

        The source lines generally look like this:
    2016-04-05 15:42:48,744 INFO  [Reporter] OVERALL 195907 objects, 200608768 bytes, 0 errors, AVG (4166.2 obj, 4.3 MB)/s, 13.3 ms latency
    2016-04-05 15:42:53,745 INFO  [Reporter] OVERALL 217671 objects, 222895104 bytes, 0 errors, AVG (4351.8 obj, 4.5 MB)/s, 13.7 ms latency
    2016-04-05 15:42:58,745 INFO  [Reporter] OVERALL 240400 objects, 246169600 bytes, 0 errors, AVG (4545.4 obj, 4.7 MB)/s, 14.1 ms latency
    2016-04-05 15:43:03,746 INFO  [Reporter] OVERALL 264017 objects, 270353408 bytes, 0 errors, AVG (4722.6 obj, 4.8 MB)/s, 14.4 ms latency
    """
    global headerPrinted
    _dt0 = None
    if cache is None and not headerPrinted:
        _line = "Time,Elapsed,# Objects,# Bytes,# Errors,AVG obj/s,AVG MB/s,AVG latency [ms]"
        if appendix is not None:
            _line = _line + ',' + ",".join(appendix.keys())
        print _line
        headerPrinted = True

    for line in fd:
        match = REGEX.search(line)
        if match:
            _dt, _objs, _sz, _errors, _objPs, _mbPs, _unit, _lat = match.groups()
            # Adjust units ...
            if _unit == 'k':
                _mbPs = float(_mbPs) / 1000
            elif _unit == 'G':
                _mbPs = float(_mbPs) * 1000
            elif _unit == '':
                _mbPs = float(_mbPs) / 10000000
            # fix Datetime
            _dt = datetime.strptime(_dt, r'%Y-%m-%d %H:%M:%S,%f')
            if not _dt0:
                _dt0 = _dt
            _duration = str(_dt - _dt0)
            v = [_dt, _duration, int(_objs), long(_sz), int(_errors), float(_objPs), float(_mbPs), float(_lat)]
            if appendix is not None:
                v.extend(appendix.values())
            if cache is not None:
                cache.append(v)
            else:
                print ",".join(str(_) for _ in v)


def process_filenames(file_name):
    """ Function processes the filename, generally looking like
        'something_<ip address>_thr<number of threads>_sz<size of objects>_something'
        :returns None if nothing matched, or ordered dictionary
    """
    global ipREGX, thrREGX, sizeREGX
    if ipREGX is None:
        ipREGX, thrREGX, sizeREGX = (
            re.compile(r"(\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4})"), re.compile(r"(?:thr|thread[s]*)(\d+)"),
            re.compile(r"(?:sz|size)(\d+)"))

    d = OrderedDict()

    def _test_and_set(regexp, label):
        m = regexp.search(file_name)
        if m:
            d[label] = m.group(1)

    _test_and_set(ipREGX, 'ip')
    _test_and_set(thrREGX, 'threads')
    _test_and_set(sizeREGX, 'size')
    return None if len(d) == 0 else d


if __name__ == '__main__':
    data = None  # []
    for fname in sys.argv[1:]:
        if fname == '-':
            parse(sys.stdin, cache=data)
        else:
            with open(fname, 'rb') as fd:
                parse(fd, cache=data, appendix=process_filenames(fname))
                # data.sort()
                # print "\n".join(str(_) for _ in data)
