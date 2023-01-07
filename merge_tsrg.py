#!/usr/bin/env python3

from typing import Optional

def import_csv(path) -> dict[str, str]:
    """Import an MCP CSV file.
    :return: A dict of searge name -> deobfuscated name
    """
    with open(path, 'r') as f:
        lines = f.readlines()
    # searge,name,side,desc
    lines = [line.strip().split(',') for line in lines]
    return {line[0]: line[1] for line in lines}

def modify_tsrg(path, replacements: dict[str, str], out=None, verbose=False) -> Optional[str]:
    """Modify a TSRG file based on the given replacements.
    :return: the modified TSRG file as a string, unless out is specified
    """
    if verbose:
        print(f'Loading TSRG file {path}')
    with open(path, 'r') as f:
        lines: list[str] = f.readlines()

    lines = [line.strip('\n') for line in lines]
    output = []
    for line in lines:
        if not line.startswith('\t'):
            # Class, no modification permitted
            output.append(line)
        elif line.count(' ') == 1:
            # Field
            obf, searge = line.strip().split(' ')
            if searge in replacements:
                searge = replacements[searge]
            output.append(f'\t{obf} {searge}')
        elif line.count(' ') == 2:
            # Method
            obf, desc, searge = line.strip().split(' ')
            if searge in replacements:
                searge = replacements[searge]
            output.append(f'\t{obf} {desc} {searge}')
        else:
            # Something else, just copy it
            output.append(line)
            print(f'Unexpected line: "{line}"')

    output = '\n'.join(output)
    if out is not None:
        if verbose:
            print(f'Writing to {out}')
        with open(out, 'w') as f:
            f.write(output)
    else:
        return output

if __name__ == '__main__':
    import sys
    import os

    if len(sys.argv) != 4:
        print('Usage: python3 merge-tsrg.py <tsrg> <csv-dir> <out>')
        sys.exit(1)
    tsrg, csv_dir, out = sys.argv[1:]
    replacements = {}
    for path in os.listdir(csv_dir):
        if path.endswith('.csv'):
            print(f'Loading {path}')
            replacements.update(import_csv(os.path.join(csv_dir, path)))
    modify_tsrg(tsrg, replacements, out, verbose=True)
