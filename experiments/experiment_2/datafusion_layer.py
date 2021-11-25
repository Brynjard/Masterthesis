import os 
import sys

PARENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(PARENT_FOLDER)
import modify_labels_utils as utils

"""
This model combines the output of three models(prev, curr, next) in the dict-representation established above, and outputs a single truth for predictions. 
"""
def ex2_data_fusion(prev_model, curr_model, next_model, confidence_threshold, time_adjustment):
    predictions_dictionary = {}
    for game_url in curr_model.keys():
        url = curr_model[game_url]["url"]
        # print(url)
        current_predictions = curr_model[game_url]["predictions"]
        prev_predictions = prev_model[game_url]["predictions"]
        next_predictions = next_model[game_url]["predictions"]

        #filtering on confidence: 
        current_predictions = [p for p in current_predictions if float(p["confidence"]) >= confidence_threshold]
        prev_predictions = [p for p in prev_predictions if float(p["confidence"]) >= confidence_threshold]
        next_predictions = [p for p in next_predictions if float(p["confidence"]) >= confidence_threshold]
    

        #Adjusting time for prev and next models' predictions:
        prev_predictions = [utils.add_or_subtract_time(p, 0 - time_adjustment) for p in prev_predictions]
        next_predictions = [utils.add_or_subtract_time(p, time_adjustment) for p in next_predictions]
        
        # Merge the predictions into 1 list
        new_prev_predictions = [p for p in prev_predictions if not utils.predicted_event_exists(current_predictions=current_predictions, prediction_object_to_check=p, time_frame=10000)]
        all_predictions = current_predictions + new_prev_predictions
        new_next_predictions = [p for p in next_predictions if not utils.predicted_event_exists(current_predictions=all_predictions, prediction_object_to_check=p, time_frame=10000)]
        all_predictions = all_predictions + new_next_predictions
        
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
    dest = args[4]
    confidence_threshold = float(args[5])
    time_adjustment = int(args[6])

    utils.create_file_structure(source_prev, dest) #all models (prev, current, next) has same filestructure, so we might aswell use the prev-folder.
    prev_model = utils.create_prediction_dict(source_prev)
    current_model = utils.create_prediction_dict(source_current)
    next_model = utils.create_prediction_dict(source_next)

    prediction_dict = ex2_data_fusion(prev_model, current_model, next_model, confidence_threshold, time_adjustment)
    utils.write_predictions(dest_folder=dest, prediction_dict=prediction_dict)

