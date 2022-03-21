from email.policy import default
import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from SoccerNet.utils import getListGames
from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V2

from collections import defaultdict

def count_predictions_and_annotations(SoccerNet_path, Predictions_path, n_intervals=10, prediction_file="results_spotting.json", split="test"):

    annotation_dict = defaultdict(lambda: 0)

    confidence_levels = [i/n_intervals for i in range(0, n_intervals)]
    list_games = getListGames(split=split)
    total_number_of_annotations_in_test_set = 0
    list_of_predictions_per_confidence_level = np.zeros(n_intervals)
    overtime_goal_count = 0
    for game in list_games:
        
        ## Count labels per class
        label_files = "Labels-v2.json"
        labels = json.load(open(os.path.join(SoccerNet_path, game, label_files)))
        annotations = labels["annotations"]
        
        total_number_of_annotations_in_test_set += len(annotations)
        
        
        #####
        for annotation in labels["annotations"]:
            event = annotation["label"]
            if event in EVENT_DICTIONARY_V2:
                annotation_dict[event] = annotation_dict[event] + 1
            if event == "Goal" and int(annotation["position"]) > 2700000:
                print(f"Game: {game} gametime: {annotation['gameTime']}")
        #####

        ## Count predicions per class
        predictions_file_dict = json.load(open(os.path.join(Predictions_path, game, prediction_file)))        
        predictions = predictions_file_dict["predictions"]
        for prediction in predictions:
            confidence = float(prediction["confidence"])
            for confidence_threshold in confidence_levels:
                if confidence >= confidence_threshold:
                    curr = list_of_predictions_per_confidence_level[int(confidence_threshold * n_intervals)]
                    curr += 1
                    list_of_predictions_per_confidence_level[int(confidence_threshold * n_intervals)] = curr
    print(annotation_dict)
    print(EVENT_DICTIONARY_V2)
    return total_number_of_annotations_in_test_set, list_of_predictions_per_confidence_level

def plot_number_of_predictions_per_confidence_threshold(metric, result_array, filename):
    
    confidence_levels = np.linspace(0, 1-1/(len(result_array)), len(result_array))
    
    plt.title(f"{metric} at confidence thresholds")

    plt.xlabel("Confidence threshold")
    plt.ylabel(metric)

    plt.plot(confidence_levels, result_array, label="Our model", color="red")

    plt.xticks(np.linspace(0, 1.0, 11))
    
    plt.yticks(np.linspace(0, 600000, 7))

    plt.legend()
    plt.grid()

    plt.savefig(f"{filename}.png", bbox_inches="tight")
    plt.clf()

def plot_number_of_predictions_per_confidence_threshold_with_comparison(metric, result_array, baseline_array, filename):
    
    confidence_levels = np.linspace(0, 1-1/(len(result_array)), len(result_array))
    
    plt.title(f"{metric} at confidence thresholds")

    plt.xlabel("Confidence threshold")
    plt.ylabel(metric)

    plt.plot(confidence_levels, result_array, label="Our model", color="red")
    plt.plot(confidence_levels, baseline_array, label="Baseline", color="darkviolet")

    plt.xticks(np.linspace(0, 1.0, 11))
    
    plt.yticks(np.linspace(0, 600000, 7))

    plt.legend()
    plt.grid()

    plt.savefig(f"{filename}.png", bbox_inches="tight")
    plt.clf()

def print_table(list_of_predictions_per_confidence_level):
    confidence_levels = [i/10 for i in range(0, 10)]
    step = int(len(list_of_predictions_per_confidence_level) / 10)

    for i in range(0, len(list_of_predictions_per_confidence_level), step):
        print(f"{confidence_levels[int(i / step)]} & {list_of_predictions_per_confidence_level[i]} \\\\")

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 4:
        print(f"3 command line arguments expected, {len(args) - 1} found")
        exit()

    soccer_net_path = args[1]
    predictions_folder = args[2]
    predictions_folder_baseline = args[3]

    number_of_annotations_in_test_set, list_of_predictions_per_confidence_level = count_predictions_and_annotations(SoccerNet_path=soccer_net_path, Predictions_path=predictions_folder, n_intervals=20)
    # _, list_of_predictions_per_confidence_level_baseline = count_predictions_and_annotations(SoccerNet_path=soccer_net_path, Predictions_path=predictions_folder_baseline, n_intervals=20)
    
    # print(number_of_annotations_in_test_set)
    # print(list_of_predictions_per_confidence_level)
    # print(list_of_predictions_per_confidence_level_baseline)
    # plot_number_of_predictions_per_confidence_threshold_with_comparison("Number of predictions", list_of_predictions_per_confidence_level, list_of_predictions_per_confidence_level_baseline, "n_predictions_at_confidence_comparison")
    
    