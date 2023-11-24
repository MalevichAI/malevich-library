import argparse

import yaml

parser = argparse.ArgumentParser()
parser.add_argument('--path')
parser.add_argument('--url')
args = parser.parse_args()

data = yaml.load(open(args.path), yaml.FullLoader)
app = [*data.keys()][0]
data[app]['app']['container_ref'] = args.url
yaml.dump(data, open(args.path, 'w'))
