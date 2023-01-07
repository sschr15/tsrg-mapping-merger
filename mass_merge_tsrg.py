#!/usr/bin/env python3

from glob import glob
from merge_tsrg import import_csv, modify_tsrg
import os
import sys

if __name__ != '__main__':
    raise Exception("This is a script, not a module.")

if len(sys.argv) != 2:
    print('Usage: python3 mass_merge_tsrg.py <version>')
    sys.exit(1)

current_dir = os.path.dirname(__file__)

# Assume the MCPConfig git repo is next to this script
mcpconfig_path = os.path.join(current_dir, 'MCPConfig')
if not os.path.isdir(mcpconfig_path):
    raise Exception(f'MCPConfig not found at {mcpconfig_path}')

# Assume a csv directory is also next to this script
csv_dir = os.path.join(current_dir, 'csv')
if not os.path.isdir(csv_dir):
    raise Exception(f'CSV directory not found at {csv_dir}')

all_versions = glob(mcpconfig_path + f'/versions/*/{sys.argv[1]}/**/joined.tsrg', recursive=True) + \
    glob(mcpconfig_path + f'/versions/release/{sys.argv[1]}.*/joined.tsrg', recursive=True)

csvs = [import_csv(csv) for csv in glob(csv_dir + '/*.csv')]
replacements = {}
for csv in csvs:
    replacements.update(csv)

output_dir = os.path.join(current_dir, 'mapped', sys.argv[1])
os.makedirs(output_dir, exist_ok=True)

for version in all_versions:
    version_component = version.split(os.path.sep)[-2]  # just the directory name of the joined.tsrg
    modify_tsrg(version, replacements, os.path.join(output_dir, f'{version_component}.tsrg'), verbose=True)
