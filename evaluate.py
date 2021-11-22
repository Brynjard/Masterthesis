
import os
import logging
import zipfile
import sys
import json
import time
import numpy as np
from datetime import datetime
from SoccerNet.Evaluation.ActionSpotting import evaluate
from fuse_model_output import create_prediction_dict
"""
Evaluates the performance of the predictions.
The scipt takes three arguments, the path to soccernet, the path to the output folder with the predictions and model name.
"""

def zipResults(zip_path, target_dir, filename="results_spotting.json"):            
            zipobj = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
            rootlen = len(target_dir) + 1
            for base, dirs, files in os.walk(target_dir):
                for file in files:
                    if file == filename:
                        fn = os.path.join(base, file)
                        zipobj.write(fn, fn[rootlen:])

if __name__ == '__main__':
    log_file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".log"
    logging.basicConfig(filename=log_file_name, level=logging.DEBUG)
    args = sys.argv

    if len(args) < 4:
        print(f"3 command line arguments expected, {len(args) - 1} found")
        exit()

    model_name = args[3]
    soccer_net_path =  args[1]
    split = "test"
    output_folder = args[2]
    output_results = f"results_spotting_{split}.zip"

    model_name = args[3]

    

    zipResults(zip_path = output_results,
            target_dir = os.path.join("models", model_name, output_folder),
            filename="results_spotting.json")

            
    results =  evaluate(SoccerNet_path=soccer_net_path, 
                Predictions_path=output_results,
                split="test",
                prediction_file="results_spotting.json",
                version=2)

    a_mAP = results["a_mAP"]
    a_mAP_per_class = results["a_mAP_per_class"]
    a_mAP_visible = results["a_mAP_visible"]
    a_mAP_per_class_visible = results["a_mAP_per_class_visible"]
    a_mAP_unshown = results["a_mAP_unshown"]
    a_mAP_per_class_unshown = results["a_mAP_per_class_unshown"]

    logging.info("Model name: " + model_name)
    logging.info("Best Performance at end of training ")
    logging.info("a_mAP visibility all: " +  str(a_mAP))
    logging.info("a_mAP visibility all per class: " +  str( a_mAP_per_class))
    logging.info("a_mAP visibility visible: " +  str( a_mAP_visible))
    logging.info("a_mAP visibility visible per class: " +  str( a_mAP_per_class_visible))
    logging.info("a_mAP visibility unshown: " +  str( a_mAP_unshown))
    logging.info("a_mAP visibility unshown per class: " +  str( a_mAP_per_class_unshown))

    model_output_as_dict = create_prediction_dict(output_folder)
    events_per_game = []
    for game in model_output_as_dict.keys():
        events_per_game.append(len(model_output_as_dict[game]["predictions"]))
    avg = sum(events_per_game) / len(events_per_game)
    logging.info("Average number of events per game: {}".format(avg))

    print("Model name: " + model_name)
    print("Best Performance at end of training ")
    print("a_mAP visibility all: " +  str(a_mAP))
    print("a_mAP visibility visible: " +  str( a_mAP_visible))
    print("a_mAP visibility all per class: " +  str( a_mAP_per_class))
    print("a_mAP visibility visible per class: " +  str( a_mAP_per_class_visible))
    print("a_mAP visibility unshown: " +  str( a_mAP_unshown))
    print("a_mAP visibility unshown per class: " +  str( a_mAP_per_class_unshown))