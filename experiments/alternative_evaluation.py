import os
import numpy as np

from SoccerNet.utils import getListGames
from SoccerNet.Evaluation.utils import LoadJsonFromZip, EVENT_DICTIONARY_V2, INVERSE_EVENT_DICTIONARY_V2
from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V1, INVERSE_EVENT_DICTIONARY_V1
from SoccerNet.Evaluation.ActionSpotting import label2vector, predictions2vector, compute_class_scores, compute_mAP, delta_curve, average_mAP
import glob
import json
import zipfile
from tqdm import tqdm

def evaluate_no_delta(SoccerNet_path, Predictions_path, prediction_file="results_spotting.json", split="test", version=2, framerate=None, metric="loose"):
    framerate = 2
    list_games = getListGames(split=split)
    targets_numpy = list()
    detections_numpy = list()
    closests_numpy = list()

    
    ## dict wit
    


    for game in tqdm(list_games):

        # Load labels
        if version==2:
            label_files = "Labels-v2.json"
            num_classes = 17
        if version==1:
            label_files = "Labels.json"
            num_classes = 3
        if zipfile.is_zipfile(SoccerNet_path):
            labels = LoadJsonFromZip(SoccerNet_path, os.path.join(game, label_files))
        else:
            labels = json.load(open(os.path.join(SoccerNet_path, game, label_files)))
        # convert labels to vector
        label_half_1, label_half_2 = label2vector(
            labels, num_classes=num_classes, version=version)
        print(label_half_1.shape)
        # print(version)
        # print(label_half_2)



        # infer name of the prediction_file
        if prediction_file == None:
            if zipfile.is_zipfile(Predictions_path):
                with zipfile.ZipFile(Predictions_path, "r") as z:
                    for filename in z.namelist():
                        #       print(filename)
                        if filename.endswith(".json"):
                            prediction_file = os.path.basename(filename)
                            break
            else:
                for filename in glob.glob(os.path.join(Predictions_path,"*/*/*/*.json")):
                    prediction_file = os.path.basename(filename)
                    # print(prediction_file)
                    break

        # Load predictions
        if zipfile.is_zipfile(Predictions_path):
            predictions = LoadJsonFromZip(Predictions_path, os.path.join(game, prediction_file))
        else:
            predictions = json.load(open(os.path.join(Predictions_path, game, prediction_file)))
        # convert predictions to vector
        predictions_half_1, predictions_half_2 = predictions2vector(predictions, num_classes=num_classes, version=version)

        targets_numpy.append(label_half_1)
        targets_numpy.append(label_half_2)
        detections_numpy.append(predictions_half_1)
        detections_numpy.append(predictions_half_2)

        ## Filter on confidence?
        ## count number of predictions per class
        ## count number of labels per class
        ## Calculate TP
        ## Add these numbers to global 

        

        closest_numpy = np.zeros(label_half_1.shape)-1 #10800 x 17 with -1 values.
        #Get the closest action index
        for c in np.arange(label_half_1.shape[-1]): #for each class (17 times..)
            indexes = np.where(label_half_1[:,c] != 0)[0].tolist() #index of Every frame in first half that is annotated with this class.. 
            if len(indexes) == 0 : #If we have no annotations in first half..
                continue
            indexes.insert(0,-indexes[0])
            indexes.append(2*closest_numpy.shape[0])
            for i in np.arange(len(indexes)-2)+1: #For all frames annotated with c..
                start = max(0,(indexes[i-1]+indexes[i])//2)
                stop = min(closest_numpy.shape[0], (indexes[i]+indexes[i+1])//2)
                closest_numpy[start:stop,c] = label_half_1[indexes[i],c]
                exit()
        
        closests_numpy.append(closest_numpy)

        closest_numpy = np.zeros(label_half_2.shape)-1
        for c in np.arange(label_half_2.shape[-1]):
            indexes = np.where(label_half_2[:,c] != 0)[0].tolist()
            if len(indexes) == 0 :
                continue
            indexes.insert(0,-indexes[0])
            indexes.append(2*closest_numpy.shape[0])
            for i in np.arange(len(indexes)-2)+1:
                start = max(0,(indexes[i-1]+indexes[i])//2)
                stop = min(closest_numpy.shape[0], (indexes[i]+indexes[i+1])//2)
                closest_numpy[start:stop,c] = label_half_2[indexes[i],c]
        closests_numpy.append(closest_numpy)