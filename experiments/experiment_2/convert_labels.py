import os
from collections import defaultdict, Counter
import json
import shutil

def convert_to_previous_labels(orig_labels_path, new_labels_path):
    #shutil.copyfile(orig_labels_path, new_labels_path)
    
    file = open(orig_labels_path)
    data = json.load(file)
    print(data)
    annotations = data["annotations"]
    for i, annotation in enumerate(annotations):
        print("i: {}".format(i))
        print(annotation)
        if i > 0:
            annotation["label"] = annotation[i-1]["label"]
            annotation["team"] = annotation[i-1]["team"]
        
    
    with open(new_labels_path, 'w') as f:
        json.dump(data, f, indent=4)
        

        


#------------------ FETCHING FILEPATHS ------------------
currentDir = os.path.dirname(os.path.realpath('__file__'))
ORIG_LABELS_PATH = os.path.join(currentDir, "../../original_labels")
NEW_LABELS_PATH = os.path.join(currentDir, "new_labels/")

#------------------ CONVERTING LABELS ------------------
leagues = os.listdir(ORIG_LABELS_PATH)
for league in leagues:
    seasons_path = ORIG_LABELS_PATH + "/" + league
    if (seasons_path.endswith("DS_Store")):
        break
    seasons = os.listdir(seasons_path)
    for season in seasons:
        matches_path = seasons_path + "/" + season
        if (matches_path.endswith("DS_Store")):
            break
        matches = os.listdir(matches_path)
        for match in matches:
            match_path = matches_path + "/" + match
            if (matches_path.endswith("DS_Store")):
                break
            labels_path = match_path + "/" + "Labels-v2.json"
            previous_label_path = NEW_LABELS_PATH + "/previous_labels.json"
            convert_to_previous_labels(labels_path, previous_label_path)
            quit()
            





