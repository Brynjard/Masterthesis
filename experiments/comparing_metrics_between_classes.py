from re import A
import sys
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
from alternative_evaluation import create_scores_dict
from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V2

def create_plot_classes(metric, result_array, filename):
    
    confidence_levels = np.linspace(0, 1-1/(len(result_array[0])), len(result_array[0]))
    
    plt.title(f"{metric} at confidence thresholds")

    plt.xlabel("Confidence threshold")
    plt.ylabel(metric)
    ax = plt.gca()
    ax.set_prop_cycle(color=['red', 'green', 'blue'])

    for i, array in enumerate(result_array):
        plt.plot(confidence_levels, array, label=list(EVENT_DICTIONARY_V2.keys())[i])
    
    
    fig = plt.gcf()
    fig.set_size_inches(10, 5)
    plt.xticks(np.linspace(0, 1.0, 11))
    plt.yticks(np.linspace(0, 1.0, 11))
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid()
    plt.savefig(fname=f"{filename}.png", bbox_inches="tight")
    plt.clf()

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 3:
        print(f"2 command line arguments expected, {len(args) - 1} found")
        exit()
    
    # print(list(EVENT_DICTIONARY_V2.keys()))
    # exit()
    
    soccer_net_path = args[1]
    predictions_folder = args[2]

    scores_dict = create_scores_dict(SoccerNet_path=soccer_net_path, Predictions_path=predictions_folder)

    ## STARTING WITH PRECISION
    ## Create a list of lists with values
    list_of_lists = list()
    for event_name in EVENT_DICTIONARY_V2.keys():
        values_list = scores_dict["precision"][event_name]
        list_of_lists.append(values_list)

    # for i, array in enumerate(list_of_lists):
    #     print(f"{list(EVENT_DICTIONARY_V2.keys())[i]}: {array}")

    create_plot_classes("Precision", list_of_lists, "precision_per_class")

    # red_card_list = scores_dict["precision"]["Red card"]
    # print(red_card_list)
    # print(list(red_card_list))

    # red_card_list = np.array([0.00014662219126864852, 0.21428571428571427, 0.0, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN])
    # create_plot_classes("Precision", red_card_list, "precision_red_cards")
    
    # list_of_lists = [precisions_array_1, recalls_array_1, f1_score_array_1, precisions_array_2, recalls_array_2, f1_score_array_2]
    # for e in list_of_lists:
    #     print(list(e))

    # precisions_array_1 = [0.02662094284719312, 0.1520755990550118, 0.23675887661297124, 0.3227907923628379, 0.4158197083517455, 0.5194029098060969, 0.6231536926147705, 0.7358482000998684, 0.8877634262406526, 0.9897902097902098]
    # recalls_array_1 = [1.0, 0.9990687774378076, 0.9958760143674338, 0.9843465921688617, 0.9597357101680635, 0.9134406456476432, 0.8306505254755887, 0.7188151301494391, 0.5790874018890515, 0.31382200345882666]
    # f1_score_array_1  = [0.051861289276572846, 0.2639703340929461, 0.3825666272028073, 0.48615856329391155, 0.5802412868632708, 0.6622407972994696, 0.7120944289217084, 0.7272319425751459, 0.7009473712460751, 0.47654961112420463]
    
    # precisions_array_2 = [0.04736003158595517, 0.27400425661295225, 0.42397627682079175, 0.5685054752968999, 0.7047720678960883, 0.8241261722080137, 0.904952855749431, 0.9599039954821403, 0.9799040191961608, 0.9871915614993407]
    # recalls_array_2 = [1.0, 0.9990687774378076, 0.9953882311205712, 0.9807103897831582, 0.937164649017782, 0.8573455722584364, 0.7405436566005942, 0.6029887809853222, 0.43461487295463613, 0.23240654516429426]
    # f1_score_array_2 = [0.09043696562344598, 0.43006031915705883, 0.5946618981389495, 0.7197695800042309, 0.80452244089992, 0.8404077285866424, 0.8145348128277039, 0.7406923223574912, 0.602156483273431, 0.37623833452979183]
    
    # create_plot_classes("Precision", combined_array, "precision_per_class")
    
    # create_plot("Recall", recalls_array_1, recalls_array_2, "recall")
    # create_plot("F1 score", f1_score_array_1, f1_score_array_2, "f1_score")