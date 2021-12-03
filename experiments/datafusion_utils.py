import os 
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) #This is to make imports from parent-folder work..
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from delete_files import delete_files
from distutils.dir_util import copy_tree
import json
import copy
import math

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
"""
Takes a src-folder (which isfilled with results_spotting.json-files in the soccernet-folder struct)
and creates one prediction_dict from this folder. One prediction_dict represents the result of one 
model, on the following format: 
pred_dict = {
    game_url: {
        url: game_url
        predictions: [list_of_predictions]
    }
}
"""
def create_prediction_dict(src):
    filenames = []
    find_files_in_folders(filenames, src)
    predictions_dictionary = {}
    for filename in filenames:
        url_local, preds = extract_events_from_file(filename)
        relative_path = strip_filename_to_relative(filename)
        predictions_dictionary[relative_path] = {}
        predictions_dictionary[relative_path]["url"] = url_local
        predictions_dictionary[relative_path]["predictions"] = preds
    return predictions_dictionary
    

"""
Recursively finds the filenames of all nested files within a folder, src (with absolute path) and appends them to file_list.
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
Check if the prediction already exist int he current_predition list within a set time frame
"""
def predicted_event_exists(current_predictions, prediction_object_to_check, time_frame):
    min_interval = int(prediction_object_to_check["position"]) - int(time_frame / 2)
    max_interval = int(prediction_object_to_check["position"]) + int(time_frame / 2)
    event_type = prediction_object_to_check["label"]
    for prediction_object in current_predictions:
        label = prediction_object["label"]
        position = int(prediction_object["position"])
        if label == event_type and position >= min_interval and position <= max_interval:
            return True
    
    return False

def find_events_in_window(preds, window, current_position, current_half): #Window is number of seconds, current_position is milliseconds(int)
    min_interval = current_position - int(window / 2)
    max_interval = current_position + int(window / 2)
    relevant_events = []
    for p in preds:
        if int(p["position"]) >= min_interval and int(p["position"]) <= max_interval and int(p["gameTime"][0]) == current_half:
            relevant_events.append(p)
    return relevant_events




def replace_event(current_predictions, prediction_object_to_check, time_frame):
    min_interval = int(prediction_object_to_check["position"]) - int(time_frame / 2)
    max_interval = int(prediction_object_to_check["position"]) + int(time_frame / 2)
    event_type = prediction_object_to_check["label"]
    index_switch_objects = None
    for i, prediction_object in enumerate(current_predictions):
        label = prediction_object["label"]
        position = int(prediction_object["position"])
        if label == event_type and position >= min_interval and position <= max_interval:
            if float(prediction_object["confidence"]) < float(prediction_object_to_check["confidence"]):
                index_switch_objects = i
    
    if index_switch_objects is not None:
        current_predictions[index_switch_objects] = copy.deepcopy(prediction_object_to_check)

"""
Takes a prediction json-object as input, and returns the game-half and time of the prediction as numbers:
half, minute, second
"""
def convert_timestring_to_nums(pred_object):
    time_string = pred_object["gameTime"]
    half = int(time_string[0])
    time_split = time_string[4:].split(":")
    minute = int(time_split[0])
    second = int(time_split[1])
    return half, minute, second

def convert_nums_to_timestring(half, minute, second):
    time_string = ""
    time_string += str(half) + " - " #adding half..
    time_string += str(minute) + ":" #adding minute
    time_string += str(second) #adding seconds
    return time_string

"""
Takes a pred_object and a time_adjustment and adjusts the time(both gameTime and position) of that prediction object. 
If time_adjustment is < 0, the time is adjusted "back in time", and if its positive, we are shifting time in the future.
"""
def add_or_subtract_time(pred_object, time_adjustment):
    half, _, _ = convert_timestring_to_nums(pred_object)
    new_position = int(pred_object["position"]) + time_adjustment
    minute = (new_position / 1000) / 60

    if minute % 1 == 0:
        second = 0
    else:
        second = math.floor(60 * math.modf(minute)[0])
    minute = int(minute)
    pred_object["gameTime"] = convert_nums_to_timestring(half, minute, second)
    pred_object["position"] = new_position
        
    return pred_object

def convert_position_to_gamestring(position):
    minute = (position / 1000) / 60

    if minute % 1 == 0:
        second = 0
    else:
        second = math.floor(60 * math.modf(minute)[0])
    if len(str(int(minute))) == 1:
        str_minute = "0" + str(int(minute))
    else:
        str_minute = str(int(minute))
    if len(str(int(second))) == 1:
        str_second = "0" + str(int(second))
    else:
        str_second = str(int(second))
    return str_minute + ":" + str_second


"""
This function takes a list of predictions, and filters out all events that have a name included in @invalid_events
"""

INVALID_EVENTS_PAST_MODEL = ["Throw-in", "Yellow->red card", "Kick-off", "Indirect free-kick", "Clearance", "Corner", "Substitution", "Direct free-kick", "Yellow card", "Shots on target", "Shots off target", "Red card", "Penalty"]

INVALID_EVENTS_FUTURE_MODEL = ["Ball out of play", "Foul", "Substitution", "Offside", "Shots on target", "Shots off target", "Goal"]

def filter_prediction_on_events(preds, invalid_events):
    filtered = [p for p in preds if p["label"] not in invalid_events]
    return filtered

def sort_predictions_on_position(preds):
    sorted_preds = sorted(preds, key=lambda p: int(p["gameTime"][0]))
    halftime_i = 0
    for i, p in enumerate(sorted_preds):
        if p["gameTime"][0] == "2":
            halftime_i = i
            break
    sorted_preds[:halftime_i] = sorted(sorted_preds[:halftime_i], key=lambda p: int(p["position"]))
    sorted_preds[halftime_i:] = sorted(sorted_preds[halftime_i:], key=lambda p: int(p["position"]))
    return sorted_preds
