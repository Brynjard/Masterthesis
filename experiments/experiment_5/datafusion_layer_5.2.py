import os, sys
import inspect
from distutils.dir_util import copy_tree
import json
from numpy.lib.function_base import average, median
PARENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(PARENT_FOLDER)
from evaluate import evaluate_predictions
from event_relation_timing import event_time_past, event_time_future, calculate_time_between_events
import datafusion_utils as utils

def get_preds_within_window(min_pos, max_pos, preds, half):
    return [p for p in preds if int(p["position"]) >= min_pos and int(p["position"]) <= max_pos and int(p["gameTime"][0]) == half]

def get_most_confident_preds(min_pos, max_pos, past_p, current_p, future_p, half):
    #First we have to get the relevant events within timewindow: 
    past_p = get_preds_within_window(min_pos, max_pos, past_p, half)
    current_p = get_preds_within_window(min_pos, max_pos, current_p, half)
    future_p = get_preds_within_window(min_pos, max_pos, future_p, half)

    #Put them in the right bins: 
    prediction_bins = {
        "Throw-in": [],
        "Ball out of play": [],
        "Kick-off": [],
        "Indirect free-kick": [],
        "Clearance": [],
        "Foul": [],
        "Corner":[],
        "Substitution": [],
        "Offside": [],
        "Direct free-kick": [],
        "Yellow card": [],
        "Shots on target": [],
        "Shots off target": [],
        "Goal": [],
        "Red card": [],
        "Penalty": [],
        "Yellow->red card": []
    }
    for p in past_p:
        prediction_bins[p["label"]].append(p)
    for p in current_p: 
        prediction_bins[p["label"]].append(p)
    for p in future_p:
        prediction_bins[p["label"]].append(p)
    
    for k in prediction_bins.keys():
        prediction_bins[k].sort(key=lambda p: float(p["confidence"]), reverse=True)
    
    candidate_preds = []
    for k in prediction_bins.keys():
        if len(prediction_bins[k]) > 0:
            candidate_preds.append(prediction_bins[k][0])
    return candidate_preds

def filter_on_confidence(t_window, past_p, current_p, future_p): #Returns a list of predictions after filtering on confidence, according to 5.2
    confident_preds = []
    #Iterate over t_window from 0:00 to 50:00 for both halves of a match. 
    #For a given window t_window: Gather all events from all predictions into separate "bins". Remove every one, but the one with the most confidence
    t_window = t_window * 1000
    #half 1:
    for i in range(0, 3000000, t_window): 
        min_i = i
        max_i = i + t_window
        preds_in_window = get_most_confident_preds(min_i, max_i,past_p, current_p, future_p, 1)
        print("1st half: For window: {} - {} we have {} preds.".format(min_i, max_i, len(preds_in_window)))
        if len(preds_in_window) > 0:
            for p in preds_in_window:
                confident_preds.append(p)
    #for second half:
    for i in range(0, 300000, t_window):
        min_i = i
        max_i = i + t_window
        preds_in_window = get_most_confident_preds(min_i, max_i,past_p, current_p, future_p, 2)
        print("2nd half: For window: {} - {} we have {} preds.".format(min_i, max_i, len(preds_in_window)))
        if len(preds_in_window) > 0:
            for p in preds_in_window:
                confident_preds.append(p)
    return confident_preds


"""
Derived from datafusion_layer from ex4:
"""
def data_fusion(prev_model, curr_model, next_model, timeframe, event_time_future_dict, event_time_past_dict, filter_time_window):
    predictions_dictionary = {}
    for game_url in curr_model.keys():
        url = curr_model[game_url]["url"]
        
        current_predictions = curr_model[game_url]["predictions"]
        prev_predictions = prev_model[game_url]["predictions"]
        next_predictions = next_model[game_url]["predictions"]

        #Filtering prev and next predictions on events that are invalid for them:
        prev_predictions = utils.filter_prediction_on_events(prev_predictions, utils.INVALID_EVENTS_PAST_MODEL)
        next_predictions = utils.filter_prediction_on_events(next_predictions, utils.INVALID_EVENTS_FUTURE_MODEL)
    
        #Prev only considers: events_time_past
        #Next only considers: events_time_future

        #Adjusting time for prev and next models' predictions:
        prev_predictions = [utils.add_or_subtract_time(p, 0 - int(event_time_future_dict[p["label"]])) for p in prev_predictions]
        next_predictions = [utils.add_or_subtract_time(p, int(event_time_past_dict[p["label"]])) for p in next_predictions]

        #Removing past-predictions that have negative position, these are inadmissible:
        prev_predictions = [p for p in prev_predictions if float(p["position"]) >= 0]

        for p in prev_predictions:
            p["model"] = "past"
        
        for p in next_predictions:
            p["model"] = "future"
        
        for p in current_predictions:
            p["model"] = "current"

        # Merge the predictions into 1 list
        """new_prev_predictions = [p for p in prev_predictions if not utils.predicted_event_exists(current_predictions=current_predictions, prediction_object_to_check=p, time_frame=timeframe*1000)]
        all_predictions = current_predictions + new_prev_predictions
        new_next_predictions = [p for p in next_predictions if not utils.predicted_event_exists(current_predictions=all_predictions, prediction_object_to_check=p, time_frame=timeframe*1000)]
        all_predictions = all_predictions + new_next_predictions
        """

        #Merging all predictions into one, after filtering on confidence: 
        all_predictions = filter_on_confidence(filter_time_window, prev_predictions, current_predictions, next_predictions)
        #all_predictions = prev_predictions + next_predictions + current_predictions
        
        # Add game to the prediction dict    
        predictions_dictionary[game_url] = {}
        predictions_dictionary[game_url]["url"] = url
        predictions_dictionary[game_url]["predictions"] = all_predictions
        
    
    return predictions_dictionary


if __name__ == '__main__':
    
    
    args = sys.argv
    if len(args) < 8:
        print(f" 7 command line arguments expected, {len(args) - 1} found")
        exit()
    #Have to take these arguments: Source_prev source_curr source_next output_folder:
    source_prev = args[1] # ouput_test folder for past model
    source_current = args[2] # ouput_test folder for current model
    source_next = args[3] # ouput_test folder for future model
    source_labels = args[4] # path to soccernet. Root folder for features/labels. Parent folder of leagues
    dest = args[5] # Destination/output folder for the combined predictions
    timeframe = float(args[6]) # The time period in which only one event of the same class can happen.
    model_name = args[7] # Model name of own choosing
    filter_time_window = args[8]

    utils.create_file_structure(source_prev, dest) #all models (prev, current, next) has same filestructure, so we might aswell use the prev-folder.
    prev_model = utils.create_prediction_dict(source_prev)
    current_model = utils.create_prediction_dict(source_current)
    next_model = utils.create_prediction_dict(source_next)
    
    #Get average time between events, according to ex3:
    calculate_time_between_events(source_labels)

    for event in event_time_future.keys():
        event_time_future[event] = median(event_time_future[event])
    for event in event_time_past.keys():
        event_time_past[event] = median(event_time_past[event])
    """print("PRINTING EVENT MEDIANS:")
    print(event_time_future)
    ob = {
            "gameTime": "2 - 2:3",
            "label": "Kick-off",
            "position": "123500",
            "half": "2",
            "confidence": "0.9871262907981873"
        }
    print("Adding {} time".format(event_time_future["Goal"]))
    utils.add_or_subtract_time(ob, event_time_future["Goal"])
    print("New time: {}".format(ob["gameTime"]))
    print("New pos: {}".format(ob["position"]))"""
    
    prediction_dict = data_fusion(prev_model, current_model, next_model, timeframe, event_time_future, event_time_past, int(filter_time_window))
    """utils.write_predictions(dest_folder=dest, prediction_dict=prediction_dict)
    evaluate_predictions(soccer_net_path=source_labels,
                            output_folder=dest,
                            model_name=model_name)"""
