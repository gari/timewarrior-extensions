#!/usr/bin/env python

import sys
import json
import re
from datetime import datetime
from datetime import timedelta

# Skip the configuration settings.
for line in sys.stdin:
    # print(line)
    if re.match("temp.report.tags", line):
        print(line)
    if line == '\n':
        break;

# Extract the JSON.
doc = ''
for line in sys.stdin:
    doc += line

total_active_time = 0

j = json.loads(doc)
for object in j:
    fix = timedelta(hours=3)
    start = object['start']
    if 'end' in object:
        end = object['end']
        end_time = datetime.strptime(end, '%Y%m%dT%H%M%SZ')
        end_time += fix
    else:
        end = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        end_time = datetime.strptime(end, '%Y%m%dT%H%M%SZ')
    start_time = datetime.strptime(start, '%Y%m%dT%H%M%SZ')
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
