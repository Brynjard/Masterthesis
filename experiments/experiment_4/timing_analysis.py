import os, sys
from distutils.dir_util import copy_tree
import json
import inspect
from copy import deepcopy
from event_relation_timing import event_time_past, event_time_future, calculate_time_between_events
from numpy.lib.function_base import average, median
from evaluate import evaluate_predictions

PARENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(PARENT_FOLDER)

import datafusion_utils as utils

from datafusion_layer import data_fusion


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

    #Get average time between events, according to ex3:
    calculate_time_between_events(source_labels)
    event_time_future_original = deepcopy(event_time_future)
    event_time_past_original = deepcopy(event_time_past)

    for i in range(-2, 3, 1):

        destination_folder = dest + str(i + 3)

        utils.create_file_structure(source_prev, destination_folder) #all models (prev, current, next) has same filestructure, so we might aswell use the prev-folder.
        prev_model = utils.create_prediction_dict(source_prev)
        current_model = utils.create_prediction_dict(source_current)
        next_model = utils.create_prediction_dict(source_next)

        if i == 0:
            continue
        print(f"Percent of median: {(1 + i * 0.1)}")
        for event in event_time_future_original.keys():
            event_time_future[event] = median(event_time_future_original[event]) * (1 + i * 0.1)
        for event in event_time_past_original.keys():
            event_time_past[event] = median(event_time_past_original[event]) * (1 + i * 0.1)
        prediction_dict = data_fusion(prev_model, current_model, next_model, timeframe, event_time_future, event_time_past)

        utils.write_predictions(dest_folder=destination_folder, prediction_dict=prediction_dict)


        evaluate_predictions(soccer_net_path=source_labels,
                                output_folder=destination_folder,
                                model_name=model_name)
