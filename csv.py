#!/usr/bin/env python

import sys
import json
from datetime import datetime
from datetime import timedelta

DATEFORMAT = '%Y%m%dT%H%M%SZ'

# Extract the configuration settings.
header = 1
configuration = dict()
body = ''
for line in sys.stdin:
    if header:
        if line == '\n':
            header = 0
        else:
            fields = line.strip().split(': ', 2)
            if len(fields) == 2:
                configuration[fields[0]] = fields[1]
            else:
                configuration[fields[0]] = ''
    else:
        body += line

# Sum the second tracked by tag.
totals = dict()
j = json.loads(body)
for object in j:
    start = datetime.strptime(object['start'], DATEFORMAT)

    if 'end' in object:
        end = datetime.strptime(object['end'], DATEFORMAT)
    else:
        end = datetime.utcnow()

    tracked = end - start
    # print(object['tags'])
    for tag in object['tags']:
        # print(tag)
        if tag in totals:
            totals[tag] += tracked
        else:
            totals[tag] = tracked

# Extract the JSON.
# doc = ''
# for line in sys.stdin:
#     doc += line

total_active_time = 0

j = json.loads(body)
for object in j:
    fix = timedelta(hours=3)
    start = object['start']
    if 'end' in object:
        end = object['end']
        end_time = datetime.strptime(end, DATEFORMAT)
        end_time += fix
    else:
        end = datetime.now().strftime(DATEFORMAT)
        end_time = datetime.strptime(end, DATEFORMAT)
    start_time = datetime.strptime(start, DATEFORMAT)
    start_time += fix
    line = '"%s",' % start_time
    line += '"%s"' % end_time
    spent = end_time - start_time
    line += ',"%s"' % spent
    if 'tags' in object:
        for tag in object['tags']:
            li = tag
            line += ',"%s"' % str(li)
    print(line)
