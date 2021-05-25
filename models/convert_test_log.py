#Example usage:
# python convert_test_log.py model_1/

import sys

log_lines = []
f = open(sys.argv[1] + '/001_test_log', 'r')

for line in f.readlines():
    if not line.startswith('|'):
        log_lines.append(line)
        log_lines.append('\n')
        continue
    line_type = line.split(':')[0]
    line = line.split(':')[1]
    line = line.replace(' ','') \
               .replace('|', ' ') \
               .replace('~', 'č')\
               .replace('^', 'ć')\
               .replace('#', 'dž')\
               .replace('}', 'đ')\
               .replace('{', 'š')\
               .replace('`', 'ž')
    log_lines.append(line_type + " " + line)

f.close()

with open(sys.argv[1] + '/001_test_log_hreadable', "a") as f:
    for line in log_lines:
        f.write(line)

