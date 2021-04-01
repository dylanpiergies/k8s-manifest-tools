#!/usr/bin/env python

import sys
import yaml

if len(sys.argv) == 1:
    data = yaml.load_all(sys.stdin, Loader=yaml.FullLoader)
else:
    data = []
    for path in sys.argv[1:]:
        with open(path, 'r') as f:
            data += yaml.load_all(f, Loader=yaml.FullLoader)

data = sorted(data, key=lambda doc: doc['metadata']['name'] + doc['kind'])

for datum in data:
    print('---')
    print(yaml.dump(datum))
