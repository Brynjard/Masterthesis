## Experiments for thesis.  

### /count_predictions.py:
- Script for counting the number of predictions each model (past, future, current) contributes to the combined model. Takes the folder where the merged predictions are located as parameter.
Usage:  
`python3 count_predictions.py <predictions_source_folder>`

### /datafusion_utils.py:
- A package with functions used for fusing the different models.  

### /modify_labels_utils.py:
- A package with functions used for modifying/creating new labels. New labels are used for training, the *past*, *future* and *current* models.  

### /delete_files.py:
- Script for deleting all files in a given @source_folder with @file_name.  
Usage:  
`python3 delete_files.py <source_folder> <filename>`

### /move_labels.py:
- Script to move label files with a given @filename from the @source folder to the @destination folder. The @source and @destination folders must follow the folder-structure of features for SoccerNet (league/season/match). Each label-file is moved from the match-folder in @source, into its corresponding match-folder in  @destination.  
Usage:  
`python3 movelabels.py <source> <destination> <filename>`

### /evaluate.py:
- A package with a function `evaluate_predictions` to evaluate a model.
- Can also be used as a script that takes three command line arguments:
  - @labels_folder - the root folder that contains the SoccerNet labels
  - @predictions_folder - the root folder that contain the prediction files.  
    The *labels_folder* and *predicitons_folder* should have the same foldet structure.
  - @model_name - name of your model of yuor choosing. Should be aa descriptive name.

- The script performs an evaluation of a model, given prediction files (in a folder following the structure of soccernet, filled with results_spotting.json)
Usage:  
`python3 evaluate.py <source> <destination> <filename>`
