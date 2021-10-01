#!/usr/bin/env python
from pathlib import Path
import re
from configparser import ConfigParser
from string import Template

coordHeader = '''---------------------------------
CARTESIAN COORDINATES (ANGSTROEM)
---------------------------------
'''
emptyLine = re.compile('^$', re.MULTILINE)

def getOrcaCoords(path):
    with path.open('r') as f:
        content = f.read()
        coordPos = content.rfind(coordHeader) + len(coordHeader)
        coordEndPos = emptyLine.search(content, coordPos).start()-1
        return content[coordPos:coordEndPos]

def main():
    config = ConfigParser(comment_prefixes=('#', ';'), inline_comment_prefixes=('#', ';'))
    config.read('SpecPredictGen.conf')

    orca = Path(config['paths']['orca'])
    outputPrefix = config['paths']['outputPrefix']
    outputFolder = Path(config['paths']['outputFolder'])
    outputFolder.mkdir(exist_ok=True)

    templates = Path(config['paths']['templates'])

    geometry = getOrcaCoords(orca)

    with (templates / 'ccsd.tmpl').open('r') as f:
        ccsd = Template(f.read()).substitute({
            **config['common'],
            **config['ccsd'],
            'geometry': geometry
        })
        with (outputFolder / f'{outputPrefix}_ccsd.inp').open('w') as ccsdInp:
            ccsdInp.write(ccsd)

    with (templates / 'gs.tmpl').open('r') as f:
        gs = Template(f.read()).substitute({
            **config['common'],
            **config['gs'],
            'geometry': geometry
        })
        with (outputFolder / f'{outputPrefix}_gs.inp').open('w') as gsInp:
            gsInp.write(gs)

    with (templates / 'sx.tmpl').open('r') as f:
        tmpl = f.read()
        n = int(config['common']['nroots'])
        for i in range(1, n+1):
            sx = Template(tmpl).substitute({
                **config['common'],
                **config['sx'],
                'iroot': i,
                'geometry': geometry,
                'prefix': outputPrefix
            })
            with (outputFolder / f'{outputPrefix}_s{i}.inp').open('w') as sxInp:
                sxInp.write(sx)

if __name__ == '__main__':
    main()