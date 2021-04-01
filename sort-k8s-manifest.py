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


def sort_containers_envs(containers):
    for container in containers:
        if 'env' in container:
            container['env'] = sorted(container['env'], key=lambda env_var: env_var['name'])


for doc in data:
    if doc['kind'] in ['Deployment', 'DeploymentConfig']:
        pod_spec = doc['spec']['template']['spec']
        if 'containers' in pod_spec:
            sort_containers_envs(pod_spec['containers'])
        if 'initContainers' in pod_spec:
            sort_containers_envs(pod_spec['initContainers'])
    print('---')
    print(yaml.dump(doc))
