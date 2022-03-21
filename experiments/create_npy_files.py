import sys
import numpy as np
from annotation_evaluation import evaluate

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 2:
        print(f"2 command line arguments expected, {len(args) - 1} found")
        exit()
    delta = int(args[1])
    
    indices = [8, 9, 10, 11, 7, 5, 6, 13, 3, 1, 14, 4, 12, 2, 0, 16, 15]
    ## Our model
    precision, precision_visible, precision_unshown, \
    recall, recall_visible, recall_unshown, \
    f1_score, f1_score_visible, f1_score_unshown, \
    true_positive, true_positive_visible, true_positive_unshown, \
    false_positive, false_positive_visible, false_positive_unshown, \
    false_negative, false_negative_visible, false_negative_unshown = evaluate("/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/original_features", "/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/haakon/ContextAwareActionSpotting/experiments/experiment_5/fusion_out", delta=delta, prediction_file="results_spotting.json", split="test",)
    
    metrics_array_our_model = np.array([precision, precision_visible, precision_unshown, \
                                recall, recall_visible, recall_unshown, \
                                f1_score, f1_score_visible, f1_score_unshown, \
                                true_positive, true_positive_visible, true_positive_unshown, \
                                false_positive, false_positive_visible, false_positive_unshown, \
                                false_negative, false_negative_visible, false_negative_unshown])

    ## Sort to get the correct
    metrics_array_our_model[:,:,:] = metrics_array_our_model[:,:,indices]

    np.save(f'/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/haakon/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_our_model_delta_{delta}.npy', metrics_array_our_model)

    ## Baseline
    precision, precision_visible, precision_unshown, \
    recall, recall_visible, recall_unshown, \
    f1_score, f1_score_visible, f1_score_unshown, \
    true_positive, true_positive_visible, true_positive_unshown, \
    false_positive, false_positive_visible, false_positive_unshown, \
    false_negative, false_negative_visible, false_negative_unshown = evaluate("/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/original_features", "/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/models/ex4_NetVLAD++_original_linlayer/outputs_test/", delta=delta, prediction_file="results_spotting.json", split="test",)
    
    metrics_array_baseline = np.array([precision, precision_visible, precision_unshown, \
                                recall, recall_visible, recall_unshown, \
                                f1_score, f1_score_visible, f1_score_unshown, \
                                true_positive, true_positive_visible, true_positive_unshown, \
                                false_positive, false_positive_visible, false_positive_unshown, \
                                false_negative, false_negative_visible, false_negative_unshown])

    metrics_array_baseline[:,:,:] = metrics_array_baseline[:,:,indices]


    np.save(f'/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/haakon/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_baseline_delta_{delta}.npy', metrics_array_baseline)
    
    