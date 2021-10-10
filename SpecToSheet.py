#!/usr/bin/env python
from configparser import ConfigParser
from pathlib import Path
from decimal import Decimal
import csv

def getSpecData(moleculeFolder: Path, moleculeName: str):
    i = 1
    while True:
        path = (moleculeFolder / f'{moleculeName}_s{i}.spectrum')
        if not path.exists():
            break
        with path.open('r') as f:
            f.readline()
            yield (i, [tuple(Decimal(x) for x in l.split()[:2]) for l in f.readlines()])
            i += 1

def expf(v): 
    return '{:0.6e}'.format(v)
def floatf(v):
    return '{:0.6f}'.format(v)

def main():
    config = ConfigParser(comment_prefixes=('#', ';'), inline_comment_prefixes=('#', ';'))
    config.read('SpecToSheet.conf')

    moleculeName = config['paths']['moleculeName']
    moleculeFolder = Path(config['paths']['moleculeFolder'] or (Path('.') / moleculeName))

    shift = Decimal(config['vars']['shift'])

    fieldNames = ['WL (nm)', 'S1']

    for i, spec in getSpecData(moleculeFolder, moleculeName):
        if (i == 1):
            specs = {row[0]: [row[1]] for row in spec}
            rows = {row[0]: {'WL (nm)': floatf(row[0]), 'S1': expf(row[1])} for row in spec}
            wls = rows.keys()
            minWl = min(wls)
        else:
            for row in spec:
                wl = row[0]
                st = row[1]
                if wl >= minWl and wl in rows:
                    key = f'S{i}'
                    rows[wl][key] = expf(st)
                    specs[wl].append(st)
                    if key not in fieldNames:
                        fieldNames.append(key)
                elif wl >= minWl:
                    print(f'WARNING: Wavelength {wl} in S{i} not matched')
    
    maxSpec = 0
    specTotals = {}

    for wl in rows:
        specTotals[wl] = sum(specs[wl])
        rows[wl]['S(tot)'] = expf(specTotals[wl])
    
    maxSpec = max(specTotals[wl] for wl in specTotals)

    for wl in rows:
        rows[wl]['Normalized'] = expf(specTotals[wl] / maxSpec)
        rows[wl]['Shifted'] = floatf(wl + shift)

    fieldNames.append('S(tot)')
    fieldNames.append('Normalized')
    fieldNames.append('Shifted')

    with (moleculeFolder / f'{moleculeName}.csv').open('w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(rows[wl] for wl in rows)

if __name__ == '__main__':
    main()
