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
orca = path\to\orca.out
moleculeName = MoleculeName # Molecule Name
moleculeFolder = .\MoleculeName # Where to output .inp files, defaults to the value of moleculeName in the current folder
hessFileName = MoleculeName_gs.hess # Name of .hess file to target, defaults to {moleculeName}_gs.hess
```

6. Edit all other fields as needed. 

7. Run `SpecPredictGen.py`, the generated files will be created in the `moleculeFolder` 

## SpecToSheet Usage

After generating your .spectrum files, will create a .csv out of the data

1. Fill out `[paths]` like so:
```
moleculeName = MoleculeName
moleculeFolder = .\MoleculeName # defaults to the value of moleculeName in the current folder
```

2. Edit `[vars]` as needed

3. Run `SpecToSheet.py`, the generated file will be output as MoleculeName.csv in the `moleculeFolder`


## License
[MIT](https://choosealicense.com/licenses/mit/)