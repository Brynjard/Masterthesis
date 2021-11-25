## Experiments for thesis. 

### /experiments:
- Contains all scripts and source code for different experiments. 


### /original_labels:
- Contains original labels for soccernet-v2. Should not be touched.

### /delete_files.py:
- Script for deleting all files in a given @source_folder with @file_name.

### /move_labels.py:
- Given a folder of labels (following folder-structure of features for soccer-net) and a folder of features(following folder-structure of features for soccernet) this script copies the labels of @source and puts each label-file into its corresponding match-folder in the feature folder.  

### /evaluate.py:
- Given a models predictions (in a folder following the structure of soccernet, filled with results_spotting.json)
this script performs an evaluation of the model. 
