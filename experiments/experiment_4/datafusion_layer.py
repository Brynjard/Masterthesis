import os, sys
from distutils.dir_util import copy_tree
import json
import inspect
from event_relation_timing import event_time_past, event_time_future, calculate_time_between_events
from numpy.lib.function_base import average, median
from evaluate import evaluate_predictions

PARENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(PARENT_FOLDER)

import datafusion_utils as utils




"""
Actual datafusion-logic for ex4:
"""
def data_fusion(prev_model, curr_model, next_model, timeframe):
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
        
        prev_predictions = [utils.add_or_subtract_time(p, 0 - int(event_time_future[p["label"]])) for p in prev_predictions]
        next_predictions = [utils.add_or_subtract_time(p, int(event_time_past[p["label"]])) for p in next_predictions]
        #We will not use prev_predictions where the subtracted time is less than 0 for position:
        prev_predictions = [p for p in prev_predictions if (int(p["position"]) - int(event_time_future[p["label"]])) >= 0]
        #Sorting predictions on position:

        current_predictions = utils.sort_predictions_on_position(current_predictions)
        prev_predictions = utils.sort_predictions_on_position(prev_predictions)
        next_predictions = utils.sort_predictions_on_position(next_predictions)
        #Lets say one half is 55 minutes = 3300000 ms.
        min_pos = 0
        max_pos = timeframe*1000
        while max_pos <= 3300000:
            prev_w = utils.find_events_in_window(prev_predictions, min_pos, max_pos, 1)
            current_w = utils.find_events_in_window(current_predictions, min_pos, max_pos, 1)
            next_w = utils.find_events_in_window(next_predictions, min_pos, max_pos, 1)
            utils.pseudo_borda_count(prev_w, current_w, next_w)
            min_pos += timeframe*1000
            max_pos += timeframe*1000

        min_pos = 0
        max_pos = timeframe*1000
        while max_pos <= 3300000:
            prev_w = utils.find_events_in_window(prev_predictions, min_pos, max_pos, 2)
            current_w = utils.find_events_in_window(current_predictions, min_pos, max_pos, 2)
            next_w = utils.find_events_in_window(next_predictions, min_pos, max_pos, 2)
            utils.pseudo_borda_count(prev_w, current_w, next_w)
            min_pos += timeframe*1000
            max_pos += timeframe*1000
            
        # Merge the predictions into 1 list
        new_prev_predictions = [p for p in prev_predictions if not utils.predicted_event_exists(current_predictions=current_predictions, prediction_object_to_check=p, time_frame=timeframe*1000)]
        all_predictions = current_predictions + new_prev_predictions
        new_next_predictions = [p for p in next_predictions if not utils.predicted_event_exists(current_predictions=all_predictions, prediction_object_to_check=p, time_frame=timeframe*1000)]
        all_predictions = all_predictions + new_next_predictions
        ## Add game to the prediction dict    

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

    prediction_dict = data_fusion(prev_model, current_model, next_model, timeframe)
    


    utils.write_predictions(dest_folder=dest, prediction_dict=prediction_dict)


    evaluate_predictions(soccer_net_path=source_labels,
                            output_folder=dest,
                            model_name=model_name)
