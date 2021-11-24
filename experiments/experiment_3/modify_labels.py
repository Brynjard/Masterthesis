import sys, os, json
"""
for a given filename(that corresponds to a label..)
This function extracts the relevant information for creating another label-file.
"""
def extract_events_from_file(filepath):
    json_file = open(filepath)
    elems = json.load(json_file)
    url_local = elems["UrlLocal"]
    annotations = elems["annotations"]
    gameAwayTeam = elems["gameAwayTeam"]
    gameDate = elems["gameDate"]
    gameHomeTeam = elems["gameHomeTeam"]
    gameScore = elems["gameScore"]
    return url_local, annotations, gameAwayTeam, gameDate, gameHomeTeam, gameScore
"""
Finds all files in src-folder, and appends their name to file-list:
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
Creates a dictionary which represents the labels for soccernet. 
"""
def create_label_dict(src, label_name):
    filenames = []
    find_files_in_folders(filenames, src)
    predictions_dictionary = {}
    for filename in filenames:
        if label_name in filename:
            url_local, annotations, gameAwayTeam, gameDate, gameHomeTeam, gameScore = extract_events_from_file(filename)
            predictions_dictionary[filename] = {}
            predictions_dictionary[filename]["url"] = url_local
            predictions_dictionary[filename]["annotations"] = annotations
            predictions_dictionary[filename]["gameAwayTeam"] = gameAwayTeam
            predictions_dictionary[filename]["gameDate"] = gameDate
            predictions_dictionary[filename]["gameHomeTeam"] = gameHomeTeam
            predictions_dictionary[filename]["gameScore"] = gameScore
    return predictions_dictionary
"""
Writes labels to files with specified filename(new_file_ending) from a dictionary representing labels.
"""
def write_annotations(prediction_dict, new_file_ending):
    for filename in prediction_dict.keys():
        dirs = filename.split("/")
        new_filename = "/".join(dirs[:-1]) + "/" + new_file_ending
        with open(new_filename, "x") as write_file:
            json.dump({"UrlLocal": prediction_dict[filename]["url"], "urlYoutube": "", "annotations": prediction_dict[filename]["annotations"], "gameAwayTeam": prediction_dict[filename]["gameAwayTeam"], "gameDate": prediction_dict[filename]["gameDate"], "gameHomeTeam": prediction_dict[filename]["gameHomeTeam"], "gameScore": prediction_dict[filename]["gameScore"]}, write_file)
#Filters events for next-model based on what we know about events in soccer (what precedes what, etc)
def filter_events_for_next(annotations_dict):
    for game in annotations_dict.keys():
        annotations = annotations_dict[game]["annotations"]
        invalid_labels = ["Ball out of play", "Foul", "Substitution", "Offside", "Shots on target", "Shots off target", "Goal"]
        valid_labels = []

        for annotation in annotations: 
            if annotation["label"] not in invalid_labels:
                valid_labels.append(annotation)
        annotations_dict[game]["annotations"] = valid_labels
#Filters events for prev-model based on what we know about events in soccer (what precedes what, etc)
def filter_events_for_prev(annotations_dict):
    for game in annotations_dict.keys():
        annotations = annotations_dict[game]["annotations"]
        invalid_labels = ["Throw-in", "Yellow->red card", "Kick-off", "Indirect free-kick", "Clearance", "Corner", "Substitution", "Direct free-kick", "Yellow card", "Shots on target", "Shots off target", "Red card", "Penalty"]
        valid_labels = []

        for annotation in annotations: 
            if annotation["label"] not in invalid_labels:
                valid_labels.append(annotation)
        annotations_dict[game]["annotations"] = valid_labels

if __name__ == '__main__':
    args = sys.argv
    label_src =  args[1]
    #Use labels from ex2. to create label-dictionaries:
    prev_dict = create_label_dict(label_src, "Labels-v2-previous.json")
    next_dict = create_label_dict(label_src, "Labels-v2-next.json")
    #Filter labels in accordance with ex3:
    filter_events_for_next(next_dict)
    filter_events_for_prev(prev_dict)
    #Create new labels for ex3:
    write_annotations(next_dict, "Labels-v2-next-ex3.json")
    write_annotations(prev_dict, "Labels-v2-previous-ex3.json")
