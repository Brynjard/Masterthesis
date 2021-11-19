import os 
import sys
from delete_files import delete_files
from distutils.dir_util import copy_tree
import json

"""
This function takes in a folder with output-files from a trained model with a bunch of results_spotting.json-files (nested in soccernet-fashion),
before it copies this file/folder structure to the fuse_output_dir. Furthermore it deletes all the results_spotting.json-files, so that we can
create new output-files after fusing data and applying logic. 
"""
def create_file_structure(src, dest):
    if os.path.isdir(src) != True or os.path.isdir(dest) != True:
        print("ERROR: One of the supplied folders does not exist.")
    
    copy_tree(src, dest)
    delete_files(dest, "results_spotting.json")

def create_prediction_dict(src):
    filenames = []
    find_files_in_folders(filenames, src)
    predictions_dictionary = {}
    for filename in filenames:
        url_local, preds = extract_events_from_file(filenames[1])
        relative_path = strip_filename_to_relative(filename)
        predictions_dictionary[relative_path] = {}
        predictions_dictionary[relative_path]["url"] = url_local
        predictions_dictionary[relative_path]["predictions"] = preds
    return predictions_dictionary
    

"""
Recursively finds the filenames of all nested files within a folder (with absolute path)
"""
def find_files_in_folders(file_list, src):
    if os.path.isdir(src):
        sub_entries = os.listdir(src)
        for entry in sub_entries:
            path = src + "/" + entry
            find_files_in_folders(file_list, path)
    elif os.path.isfile(src):
        file_list.append(src)
        return

"""
Takes a file-name as argument, and returns two things: String in the form of urlLocal (this is just a string describing the game we have predicted)
and a list of predictions. Each prediction is a json-object with:
"gameTime": "1 - 9:19",
"label": "Penalty",
"position": "559000",
"half": "1",
"confidence": "0.030581321567296982"
"""
def extract_events_from_file(filepath):
    json_file = open(filepath)
    elems = json.load(json_file)
    url_local = elems["UrlLocal"]
    predictions = elems["predictions"]
    return url_local, predictions

"""
We want to strip the filename of the file, so we can safely create it within the same folder structure in our dest-folder as it was in our src-folder.
This function does that.
A typical (absolute) filepath for a json-file from src folder can look like this:
/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/models/ex1_NetVLAD++_linlayer/outputs_test/england_epl/2015-2016/2015-08-16 - 18-00 Manchester City 3 - 0 Chelsea/results_spotting.json

This method strips it to be this:
england_epl/2015-2016/2015-08-16 - 18-00 Manchester City 3 - 0 Chelsea/results_spotting.json
"""
def strip_filename_to_relative(filename):
    leagues = ["england_epl", "europe_uefa-champions-league", "france_ligue-1", "germany_bundesliga", "italy_serie-a", "spain_laliga"]

    for league in leagues:
        partitions = filename.partition(league)
        if partitions[1]:
            start_i = len(partitions[0])
            return filename[start_i:]


"""
Takes a dictionary on the same shape as we have represented our predictions from our src-models, and writes the correct .json-files to the correct
sub-directories in @src_folder.
"""
def write_predictions(dest_folder, prediction_dict):
    for filename in prediction_dict.keys():
        absolute_path = dest_folder + "/" + filename
        with open(absolute_path, "x") as write_file:
            json.dump({"UrlLocal": prediction_dict[filename]["url"], "predictions": prediction_dict[filename]["predictions"]}, write_file)
"""
This model combines the output of three models(prev, curr, next) in the dict-representation established above, and outputs a single truth for predictions. 
"""
def ex2_data_fusion(prev_model, curr_model, next_model):
    for game_url in curr_model.keys():
        current_predictions = curr_model[game_url]["predictions"]
        prev_predictions = prev_model[game_url]["predictions"]
        next_predictions = next_model[game_url]["predictions"]

        



if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print(f" atleast 2 command line arguments expected, {len(args) - 1} found")
        exit()
    #Have to take these arguments: Source_prev source_curr source_next output_folder:
    source_prev = args[1]
    source_current = args[2]
    source_next = args[3]
    dest = args[4]
    create_file_structure(source_prev, dest) #all models (prev, current, next) has same filestructure, so we might aswell use the prev-folder.
    prev_model = create_prediction_dict(source_prev)
    current_model = create_prediction_dict(source_current)
    next_model = create_prediction_dict(source_next)
    print("Length of prev: {}".format(len(prev_model["england_epl/2015-2016/2015-08-16 - 18-00 Manchester City 3 - 0 Chelsea/results_spotting.json"]["predictions"])))
    print("Length of current: {}".format(len(current_model["england_epl/2015-2016/2015-08-16 - 18-00 Manchester City 3 - 0 Chelsea/results_spotting.json"]["predictions"])))
    print("Length of next: {}".format(len(next_model["england_epl/2015-2016/2015-08-16 - 18-00 Manchester City 3 - 0 Chelsea/results_spotting.json"]["predictions"])))
    #write_predictions(dest, dict1)
