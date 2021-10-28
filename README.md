# SpecPredictGen

Creates ORCA input files for predicting vibronic spectra

## Usage

1. Put the folder containing all your molecule files in the `SpecPredictGen` folder (optional)

2. Edit SpecPredictGen.conf, fill `[paths]` in like so:
```
moleculeName = MoleculeName # Molecule Name, required
moleculeFolder = .\MoleculeName # Where to output .inp files, when left blank, defaults to the value of moleculeName in the `SpecPredictGen` folder
coordsFile = .\MoleculeName\MoleculeName.xyz # where your xyz file is located, when left blank, defaults to {moleculeName}.xyz in your molecule folder
hessFileName = MoleculeName_gs.hess # Name of .hess file to target, defaults to {moleculeName}_gs.hess
```

3. Edit all other fields as needed. 

4. Run `SpecPredictGen.py`, the generated files will be created in the `moleculeFolder` 

## SpecToSheet Usage

After generating your .spectrum files, will create a .csv out of the data

1. Fill out `[paths]` like so:
```
moleculeName = MoleculeName #Put the name of the file before the _sX, for example, for Caffeine_s1.spectrum, put "Caffeine" 
moleculeFolder = .\MoleculeName # Insert the Path to the folder with the .spectrum files in it.
```

2. Edit `[vars]` as needed

3. Run `SpecToSheet.py`, the generated file will be output as MoleculeName.csv in the `moleculeFolder`


## License
[MIT](https://choosealicense.com/licenses/mit/)