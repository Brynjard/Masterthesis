from re import A
import sys
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
from alternative_evaluation import evaluate_no_delta, evaluate_over_confidence_intervals
from table_creation_statistics_usecase import create_table_statistics

def create_plot(metric, result_array, baseline_array, filename):
    
    confidence_levels = np.linspace(0, 1-1/(len(result_array)), len(result_array))
    
    plt.title(f"{metric} at confidence thresholds")

    plt.xlabel("Confidence threshold")
    plt.ylabel(metric)

    plt.plot(confidence_levels, result_array, label="Our model", color="red")
    plt.plot(confidence_levels, baseline_array, label="Baseline", color="darkviolet")

    plt.xticks(np.linspace(0, 1.0, 11))
    plt.yticks(np.linspace(0, 1.0, 11))
    plt.legend()
    plt.grid()

    plt.savefig(f"{filename}.png")
    plt.clf()

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 4:
        print(f"3 command line arguments expected, {len(args) - 1} found")
        exit()

    soccer_net_path = args[1]
    predictions_folder = args[2]
    predictions_folder_baseline = args[3]

    # ##list_of_metric_our_model
    precisions_array_1, recalls_array_1, f1_score_array_1 = evaluate_over_confidence_intervals(SoccerNet_path=soccer_net_path, Predictions_path=predictions_folder, n_intervals=20)
    # # list_of_metric_baseline
    precisions_array_2, recalls_array_2, f1_score_array_2 = evaluate_over_confidence_intervals(SoccerNet_path=soccer_net_path, Predictions_path=predictions_folder_baseline, n_intervals=20)
    
    # list_of_lists = [precisions_array_1, recalls_array_1, f1_score_array_1, precisions_array_2, recalls_array_2, f1_score_array_2]
    # for e in list_of_lists:
    #     print(list(e))

    # precisions_array_1 = [0.02662094284719312, 0.1520755990550118, 0.23675887661297124, 0.3227907923628379, 0.4158197083517455, 0.5194029098060969, 0.6231536926147705, 0.7358482000998684, 0.8877634262406526, 0.9897902097902098]
    # recalls_array_1 = [1.0, 0.9990687774378076, 0.9958760143674338, 0.9843465921688617, 0.9597357101680635, 0.9134406456476432, 0.8306505254755887, 0.7188151301494391, 0.5790874018890515, 0.31382200345882666]
    # f1_score_array_1  = [0.051861289276572846, 0.2639703340929461, 0.3825666272028073, 0.48615856329391155, 0.5802412868632708, 0.6622407972994696, 0.7120944289217084, 0.7272319425751459, 0.7009473712460751, 0.47654961112420463]
    
    # precisions_array_2 = [0.04736003158595517, 0.27400425661295225, 0.42397627682079175, 0.5685054752968999, 0.7047720678960883, 0.8241261722080137, 0.904952855749431, 0.9599039954821403, 0.9799040191961608, 0.9871915614993407]
    # recalls_array_2 = [1.0, 0.9990687774378076, 0.9953882311205712, 0.9807103897831582, 0.937164649017782, 0.8573455722584364, 0.7405436566005942, 0.6029887809853222, 0.43461487295463613, 0.23240654516429426]
    # f1_score_array_2 = [0.09043696562344598, 0.43006031915705883, 0.5946618981389495, 0.7197695800042309, 0.80452244089992, 0.8404077285866424, 0.8145348128277039, 0.7406923223574912, 0.602156483273431, 0.37623833452979183]
    
    create_plot("Precision", precisions_array_1, precisions_array_2, "precision")
    create_plot("Recall", recalls_array_1, recalls_array_2, "recall")
    create_plot("F1 score", f1_score_array_1, f1_score_array_2, "f1_score")

    ## Create tables

