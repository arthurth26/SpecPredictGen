#!/usr/bin/env python
from pathlib import Path
import re
from configparser import ConfigParser
from string import Template

coordHeader = re.compile(r'^(\d+)(?:\n|\r\n?)Coordinates from [^\r\n]+(?:\n|\r\n?)', re.MULTILINE)
newLine = re.compile('(?:\n|\r\n?)', re.MULTILINE)

def getOrcaCoords(path):
    with path.open('r') as f:
        content = f.read()
        for match in coordHeader.finditer(content):
            pass
        n = int(match.group(1))
        coordPos = match.end()
        for i, endMatch in enumerate(newLine.finditer(content, coordPos), start=1):
            if i == n:
                break
        coordEndPos = endMatch.start()
        return content[coordPos:coordEndPos]

def main():
    config = ConfigParser(comment_prefixes=('#', ';'), inline_comment_prefixes=('#', ';'))
    config.read('SpecPredictGen.conf')

    moleculeName = config['paths']['moleculeName']
    moleculeFolder = Path(config['paths']['moleculeFolder'] or (Path('.') / moleculeName))
    moleculeFolder.mkdir(exist_ok=True)
    coordsFile = Path(config['paths']['coordsFile'] or (moleculeFolder / f'{moleculeName}.xyz'))

    templates = Path(config['paths']['templates'])

    geometry = getOrcaCoords(coordsFile)

    with (templates / 'ccsd.tmpl').open('r') as f:
        ccsd = Template(f.read()).substitute({
            **config['common'],
            **config['ccsd'],
            'geometry': geometry
        })
        with (moleculeFolder / f'{moleculeName}_ccsd.inp').open('w') as ccsdInp:
            ccsdInp.write(ccsd)

    with (templates / 'gs.tmpl').open('r') as f:
        gs = Template(f.read()).substitute({
            **config['common'],
            **config['gs'],
            'geometry': geometry
        })
        with (moleculeFolder / f'{moleculeName}_gs.inp').open('w') as gsInp:
            gsInp.write(gs)

    with (templates / 'sx.tmpl').open('r') as f:
        tmpl = f.read()
        n = int(config['common']['nroots'])
        hessname = config['paths']['hessFileName'] or f'{moleculeName}_gs.hess'
        if re.match('^.*\.\w+$', hessname) == None:
            hessname = hessname + '.hess'
        for i in range(1, n+1):
            sx = Template(tmpl).substitute({
                **config['common'],
                **config['sx'],
                'iroot': i,
                'geometry': geometry,
                'hessname': hessname
            })
            with (moleculeFolder / f'{moleculeName}_s{i}.inp').open('w') as sxInp:
                sxInp.write(sx)

if __name__ == '__main__':
    main()