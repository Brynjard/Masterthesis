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

def filter_on_confidence_overlap(t_window, past_p, current_p, future_p):

    last_valid_indeces = {
        "Throw-in": -1,
        "Ball out of play": -1,
        "Kick-off": -1,
        "Indirect free-kick": -1,
        "Clearance": -1,
        "Foul": -1,
        "Corner":-1,
        "Substitution": -1,
        "Offside": -1,
        "Direct free-kick": -1,
        "Yellow card": -1,
        "Shots on target": -1,
        "Shots off target": -1,
        "Goal": -1,
        "Red card": -1,
        "Penalty": -1,
        "Yellow->red card": -1
    }

    filtered_predictions = []

    t_window = int(t_window * 1000)
    all_predictions = past_p + current_p + future_p
    all_predictions.sort(key=lambda p: int(p["position"]))

    min_pos = 0
    max_pos = t_window // 2
    for p in all_predictions:
        most_confident_prediction = p
        min_pos = int(p["position"]) - (t_window // 2)
        if min_pos < 0:
            min_pos = 0

        max_pos = int(p["position"]) + (t_window // 2)
        for i in range(last_valid_indeces[p["label"]] + 1, len(all_predictions)):
            if int(all_predictions[i]["position"]) > max_pos:
                break
            elif all_predictions[i]["label"] != p["label"]:
                continue
            else:
                if float(all_predictions[i]["confidence"]) > float(p["confidence"]):
                    most_confident_prediction = all_predictions[i]
                last_valid_indeces[p["label"]] = i

        filtered_predictions.append(most_confident_prediction)
    
    return filtered_predictions

def filter_on_confidence_no_overlap(t_window, past_p, current_p, future_p):
    filtered_predictions = []

    t_window = int(t_window * 1000)
    all_predictions = past_p + current_p + future_p
    all_predictions.sort(key=lambda p: int(p["position"]))
    last_index = -1
    for i in range(0, 3300000, t_window):
        min_p = i
        max_p = i + t_window

        prediction_highest_confidence = {
                "Throw-in_1": 0,
                "Ball out of play_1": 0,
                "Kick-off_1": 0,
                "Indirect free-kick_1": 0,
                "Clearance_1": 0,
                "Foul_1": 0,
                "Corner_1":0,
                "Substitution_1": 0,
                "Offside_1": 0,
                "Direct free-kick_1": 0,
                "Yellow card_1": 0,
                "Shots on target_1": 0,
                "Shots off target_1": 0,
                "Goal_1": 0,
                "Red card_1": 0,
                "Penalty_1": 0,
                "Yellow->red card_1": 0,
                "Throw-in_2": 0,
                "Ball out of play_2": 0,
                "Kick-off_2": 0,
                "Indirect free-kick_2": 0,
                "Clearance_2": 0,
                "Foul_2": 0,
                "Corner_2":0,
                "Substitution_2": 0,
                "Offside_2": 0,
                "Direct free-kick_2": 0,
                "Yellow card_2": 0,
                "Shots on target_2": 0,
                "Shots off target_2": 0,
                "Goal_2": 0,
                "Red card_2": 0,
                "Penalty_2": 0,
                "Yellow->red card_2": 0
                }
        prediction_highest_confidence_object = {
        "Throw-in_1": None,
        "Ball out of play_1": None,
        "Kick-off_1": None,
        "Indirect free-kick_1": None,
        "Clearance_1": None,
        "Foul_1": None,
        "Corner_1":None,
        "Substitution_1": None,
        "Offside_1": None,
        "Direct free-kick_1": None,
        "Yellow card_1": None,
        "Shots on target_1": None,
        "Shots off target_1": None,
        "Goal_1": None,
        "Red card_1": None,
        "Penalty_1": None,
        "Yellow->red card_1": None,
        "Throw-in_2": None,
        "Ball out of play_2": None,
        "Kick-off_2": None,
        "Indirect free-kick_2": None,
        "Clearance_2": None,
        "Foul_2": None,
        "Corner_2":None,
        "Substitution_2": None,
        "Offside_2": None,
        "Direct free-kick_2": None,
        "Yellow card_2": None,
        "Shots on target_2": None,
        "Shots off target_2": None,
        "Goal_2": None,
        "Red card_2": None,
        "Penalty_2": None,
        "Yellow->red card_2": None
        }

        for j in range(last_index + 1, len(all_predictions)):
            if int(all_predictions[j]["position"]) > max_p:
                break
            elif int(all_predictions[j]["position"]) < min_p:
                continue
            else:        
                current_p = all_predictions[j]
                last_index = j
                if float(current_p["confidence"]) > prediction_highest_confidence[current_p["label"]+ "_" + current_p["gameTime"][0]]:
                    prediction_highest_confidence[current_p["label"] + "_" + current_p["gameTime"][0]] = float(current_p["confidence"])
                    prediction_highest_confidence_object[current_p["label"]+ "_" + current_p["gameTime"][0]] = current_p
                    last_index = j
        for c in prediction_highest_confidence_object.keys():
            if prediction_highest_confidence_object[c] is not None:
                filtered_predictions.append(prediction_highest_confidence_object[c])
    
    return filtered_predictions



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
        all_predictions = filter_on_confidence_no_overlap(filter_time_window, prev_predictions, current_predictions, next_predictions)
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
    
    prediction_dict = data_fusion(prev_model, current_model, next_model, timeframe, event_time_future, event_time_past, float(filter_time_window))
    utils.write_predictions(dest_folder=dest, prediction_dict=prediction_dict)
    """evaluate_predictions(soccer_net_path=source_labels,
                            output_folder=dest,
                            model_name=model_name)"""
