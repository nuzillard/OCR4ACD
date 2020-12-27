
# OCR4ACD

## Goal

Getting around the problem of reusing $^{13}$C NMR chemical shift values from ACD CNMR Predictor for their insertion in an ACD Databse file and subsequent compound search according to $^{13}$C NMR spectroscpic signature.
This solution uses a very basic optical character recognition (OCR) method (no AI there) that works only in the context for which it has been designed.

_____________________________________________

## Installation

Advanced Chemistry Development, Inc. (ACD/Labs, or in short, ACD) C+H NMR Predictors and DB installed. This is the only costly software piece.
[Anaconda](https://docs.anaconda.com/anaconda/install/) installed.
[RDKit](https://www.rdkit.org/docs/Install.html) and OpenCV installed, see Quercetin\\_README.txt.
My `Documents\` directory has a `PythonLib\` subdirectory in which I copy the python modules I write, such as those in `Python_Modules\`.
A copy of the `BoldFace\` directory must be also present beside of the `ocr_decode.py` module.
Ensure that the path to your `PythonLib\` is included in the value of the system `PYTHONPATH` variable or that the python modules `ocr_decode.py` and `trueACD.py` can be found by python. 

_____________________________________________

## Directories and Files

**BoldFace\\** contains the glyphs of the characters used by ACD to display chemical shift values in chemical shift tables produced by ACD CNMR Predictor.
The glyphs were produced from `Images\1.png` using `train.py`. See comments in this file.

**Images\\** contains a single .png image file, `1.png`, that is the same as `1.png` in `Myristic_knapsack\`.

**Myristic_knapsack\\** is related to `fake_acd_myristic_knapsack.sdf` that is produced by [KnapsackSearck](https://github.com/nuzillard/KnapsackSearch) (or KS) for the compounds isolated from plants of the Myristicaceae family (nutmeg, noix de muscade).
The `myristic_knapsack.sdf` file with its [nmrshiftdb2](https://nmrshiftdb.nmr.uni-koeln.de/)-predicted chemical shifts was reformatted for ACD DB with the name `fake_acd_myristic_knapsack.sdf` using the `fakeACD.py` script from KS.
The ACD DB file `fake_acd_myristic_knapsack.NMRUDB` was created by importation of `fake_acd_myristic_knapsack.sdf` for chemical shift prediction by ACD CNMR predictor
The images of the chemical shift tables for compounds 1 to 129 (with some ones missing due to a too important number of C atoms in a few molecules) were saved as `1.png` to `129.png` files according to the process described in `Quercetin\_README.txt`
These images where combined with `fake_acd_myristic_knapsack.sdf` to give `true_acd_myristic_knapsack.sdf` using `trueACD_demo.py`.
File `true_acd_myristic_knapsack.sdf` was imported in an ACD DB `named true_acd_myristic_knapsack.NMRUDB` and exported as `true_acd_myristic_knapsack_exported.sdf`.

**Oldies\\** contains files that were intermediately produced for this project.
`Links\` gives web links about image handling with OpenCV and about true OCR.
File `ocr.txt` is a scratchpad for ocr module installation and use.
When this work was started, the initial idea was to rely on the `pytesseract` OCR software and on its related python module.

**Python_Modules\\**
Module `ocr_decode.py` for my very own version of OCR that works only for image analysis of ACD NMR chemical shift tables.
Module `trueACD.py` supplements a .sdf input file to give a .sdf output file according to images of chemical shift tables.

**Quercetin\\**
Demo directory for the use of `trueACD_run.py`. See `_README.txt` inside.

**README.md**
This file.

**ocr_demo.py**
Run "python ocr_demo" to test module installation.
It decodes `Images\1.png` and displays a list of chemical shift values.
Please keep unchanged as backup copy.

**train.py**
Creates glyphs in directory `BoldFace\`, used by module `ocr_decode.py` and indirectly by module `trueACD.py`.
See comments in code for details.

**trueACD_demo.py**
Process files in directory Myristic_knapsack\.
Please do not edit. Keep safe as backup copy.

**trueACD_run.py**
Presently processes files in directory `Quercetin\`.
May be edited.
