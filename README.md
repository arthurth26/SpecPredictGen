# SpecPredictGen

Creates ORCA input files for predicting vibronic spectra

## Usage

1. Name your optimized `ORCA.out` file `[MoleculeName].out`

2. Put your optimized `ORCA.out` file into the `SpecPredictGen` folder (optional)

3. Open `SpecPredictGen.conf`

4. If your ORCA.out is in this folder, simply put
`.\MoleculeName.out` into the orca field

5. Otherwise, fill `[paths]` in like so:
```
orca = path\to\Inputfile.out
outputPrefix = MoleculeName
outputFolder = .\MoleculeName
hessFileName = NameOfHessFile.hess #optional, otherwise defaults to {outputPrefix}_gs.hess
```

6. Edit all other fields as needed. 

7. Run `SpecPredictGen.py`, the generated files will be created in the `outputFolder` 

## License
[MIT](https://choosealicense.com/licenses/mit/)