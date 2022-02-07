import os, sys
from distutils.dir_util import copy_tree
import json
import inspect
from event_relation_timing import event_time_past, event_time_future, calculate_time_between_events
from numpy.lib.function_base import average, median

PARENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(PARENT_FOLDER)

import datafusion_utils as utils


"""
Actual datafusion-logic for ex3:
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

        #Adding model-tag to predictions:
        for p in current_predictions:
            p["model"] = "current"
        
        for p in prev_predictions:
            p["model"] = "past"
        for p in next_predictions:
            p["model"] = "future"
    
        #Prev only considers: events_time_past
        #Next only considers: events_time_future

        #Adjusting time for prev and next models' predictions:
        prev_predictions = [utils.add_or_subtract_time(p, 0 - int(event_time_future[p["label"]] / 1000)) for p in prev_predictions]
        next_predictions = [utils.add_or_subtract_time(p, int(event_time_past[p["label"]] / 1000)) for p in next_predictions]

        # Merge the predictions into 1 list
        """new_prev_predictions = [p for p in prev_predictions if not utils.predicted_event_exists(current_predictions=current_predictions, prediction_object_to_check=p, time_frame=timeframe*1000)]
        all_predictions = current_predictions + new_prev_predictions
        new_next_predictions = [p for p in next_predictions if not utils.predicted_event_exists(current_predictions=all_predictions, prediction_object_to_check=p, time_frame=timeframe*1000)]
        all_predictions = all_predictions + new_next_predictions"""
        all_predictions = current_predictions + prev_predictions + next_predictions
        # Add game to the prediction dict    
        predictions_dictionary[game_url] = {}
        predictions_dictionary[game_url]["url"] = url
        predictions_dictionary[game_url]["predictions"] = all_predictions
        
    
    return predictions_dictionary


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 7:
        print(f" 6 command line arguments expected, {len(args) - 1} found")
        exit()
    #Have to take these arguments: Source_prev source_curr source_next output_folder:
    source_prev = args[1]
    source_current = args[2]
    source_next = args[3]
    source_labels = args[4]
    dest = args[5]
    timeframe = float(args[6])

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

