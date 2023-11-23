#!/usr/bin/env python
from configparser import ConfigParser
from pathlib import Path
from decimal import Decimal
import csv

def getSpecData(moleculeFolder: Path, moleculeName: str, NumOfCalc: int):
    for number_of_spec_calc in range(1,NumOfCalc+1):
        path = f'{moleculeFolder}/{moleculeName}_{number_of_spec_calc}.spectrum'
        with open(path,"r") as f:
            print(f'Parse S{number_of_spec_calc}')
            f.readline()
            yield (number_of_spec_calc, [tuple(Decimal(x) for x in l.split()[:2]) for l in f.readlines()])

def expf(v): 
    return '{:0.6e}'.format(v)
def floatf(v):
    return '{:0.6f}'.format(v)

WL_KEY = 'WL (nm)'
STOT_KEY = 'S(tot)'
NORM_KEY = 'Normalized'

def main():
    config = ConfigParser(comment_prefixes=('#', ';'), inline_comment_prefixes=('#', ';'))
    config.read('SpecToSheet.conf')

    moleculeName = config['paths']['moleculeName']
    moleculeFolder = Path(config['paths']['moleculeFolder'])

    normMin = Decimal(config['vars']['normMin'])
    normMax = Decimal(config['vars']['normMax'])
    NumOfCalc = Decimal(config['vars']['Number_of_calculations'])

    fieldNames = [WL_KEY, 'S1']

    for i, spec in getSpecData(moleculeFolder, moleculeName, int(NumOfCalc)):
        if (i == 1):
            specs = {row[0]: [row[1]] for row in spec}
            rows = {row[0]: {WL_KEY: floatf(row[0]), 'S1': expf(row[1])} for row in spec}
            wls = rows.keys()
            minWl = min(wls)
        else:
            key = f'S{i}'
            if key not in fieldNames:
                fieldNames.append(key)
            for row in spec:
                wl = row[0]
                st = row[1]
                if wl >= minWl:
                    try:
                        rows[wl][key] = expf(st)
                        specs[wl].append(st)
                    except KeyError:
                        print(f'WARNING: Wavelength {wl} in S{i} not matched to S1')
    

    fieldNames.append(STOT_KEY)
    fieldNames.append(NORM_KEY)

    maxSpec = 0
    specTotals = {}

    print('Calculate S(tot)')
    for wl in rows:
        specTotals[wl] = sum(specs[wl])
        rows[wl][STOT_KEY] = expf(specTotals[wl])
    
    print('Calculate S(max)')
    maxSpec = max( specTotals[wl] for wl in specTotals if wl >= normMin and wl <= normMax )

    print('Calculate normalized values')
    for wl in rows:
        rows[wl][NORM_KEY] = expf(specTotals[wl] / maxSpec)

    outFilePath = moleculeFolder / f'{moleculeName}.csv'
    print(f'Write {outFilePath}')
    with (outFilePath).open('w') as csvFile:
        dialect = csv.excel
        dialect.lineterminator = '\n'
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames, dialect=dialect)
        writer.writeheader()
        writer.writerows(rows[wl] for wl in rows)

if __name__ == '__main__':
    main()
