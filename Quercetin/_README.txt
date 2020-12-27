User's manual of trueACD.py

Requires ACD "C+H NMR Predictors and DB"
This manuel is therefore only useful to those who use Windows as computer OS.

Tested with Python Anaconda (version 3.6.10), rdkit (version 2020.03.1.0) and opencv (version 3.4.2)
If not installed "conda create -c rdkit -n rdkit3" then "activate rdkit3" then "conda install -c defaults opencv".

Application to quercetin
Initial file is Quercetin\quercetin2D_original.sdf, from PubChem (most probably).
This file contains data for a single compound, but this is ok.

Goal: Build an ACD DB with the structure of quercetin and its 13C NMR chemical shifts
as predicted by the ACD CNMR predictor.

Step-by-step procedure
0. Create a directory named MyQuercetin besides directory Quercetin\. Copy Quercetin\quercetin2D_original.sdf in MyQuercetin.

1. Open CNMR predictor and switch to Database (Database tab at the bootom of main window or Alt-7, Alt-Maj-7 if 7 in uppercase, as in French keyboards)

2. Create new database (DB): Database->New... Type demo as file name and select MyQuercetin as directory 
Leave password fields empty an click OK.

3. Import initial .sdf file: Database->Import... Type quercetin2D_original.sdf as file name
Check import Options and click Ok. The Import information window appears. Click Ok.

4. Copy molecule to Editor (Alt-R C).

5. The molecule has explicit H atoms. Remove them fist (nothing to do if no explicit H is there)
Tools->Remove Explicity Hydrogens. Alt-9 to Update DB. Select Update current record. Select Use given Form. Click Ok.
Copy molecule to Editor (Alt-R C) again. Clear previous contents of editor window when requested.

6. Show atom numbers with Tools->Show/Hide Atom numbers.
This is a mandatory step. You have been warned.

7. Predict chemical shifts using CNMR predictor. Alt-2 (or Alt-Maj-2).
In this case, the Select Tautomeric Forms to Use window pops up. Select Only given form. Click Ok.
A warning message appears about selected solvent (DMSO) may appear. Click Ok.

8. Show chemical shift table. Show->Table of Chemical Shifts.
The table appears. Enlarge window toward the bottom of the screen if scroll bar appear.

In this case, move the place of the window bottom line to the end of the last line in table.
Place the mouse at a place where no cell in the table has an orange-colored background and no 
red frame appears. Clicking in an empty zone of spectrum display zone may be useful.
Do not change the row height, which should be kept at its minimum.

9. Take a snapshot of the chemical shift table with Windows-Maj-S. If not already active,
click on the middle icon of the snapshot icon bar (5 icons) for window snapshot selection.
Click on the chemical shift table window to record its image.
Windows open the window of the snapshot tool on the bottom right of the screen.
Click on the window of the snapshot tool. The snapshot editor window appears.
Store the image (disk icon on the upper right of the screen.
Replace the proposed file name by the molecule index: 1.
Ensure to save the image in the MyQuercetin directory.
Close the screenshot edition window.
Check for the existence and content of file MyQuercetin\1.png

10. Return to Database window or Alt-5.

11. If the initial .sdf file contains more molecules
select the next molecule with the green arrow that points to the right side.
Go to step 4 for the current molecule. Save the snapshot using 2 (3, and so on) as file name.

12. Export DB as a .sdf file. Database->Export... Click Ok to remove the warning window.
DEMO.SDF is proposed as file name for exportation. Replace DEMO.SDF by demo (the same but lower case).

13. Edit file trueACD_run.py, placed in the same directory as the MyQuercetin directory.
Ensure that
curdir = "MyQuercetin"

14. Open an Anaconda prompt window, activate the environment in which the RDKit and OpenCV packages are installed.
Set current directory to the one that contains the trueACD_run.py script.

15. Run "python trueACD_run.py". This creates the true_acd_demo.sdf file with predicted chemical shifts inside.

16. Close current Database Database->Close

17. Create of new database from true_acd_demo.sdf. Database->New...
Use true_acd_demo for the name of the new DB. Leave all password fields empty. Click Ok.

18. Import file true_acd_demo.sdf in current DB. Databse->Import...
with true_acd_demo.sdf as file name. Accept Import Options with click Ok.
Click Ok to Import information. The chemical shifts from image file MyQuercetin\1.png appear.

19. Check imported chemical shift consistency. Database->Tools->Check Chemical Shifts.
A new column appears with calculated chemical shifts, with lines colored in green/orange/red
depending on the matching between the imported chemical shifts (from CNMR predictor)
in column "13C Shift" and those calculated for the purpose of checking in column "13C Calc".

20. Close DB and exit. Database->Close then Database->Exit.
The DB and structure editor windows have disappeared.

Epilog. In the case of quercetin, the content of the columns "13C Shift" and "13C Calc"
are rigourously the same. This is not always the case. Chemical shift values may differ from
a few ppm, leading ACD DB checker to declare as "orange" the values provided by CNMR Predictor.
