from multiprocessing import get_start_method
import numpy as np
from event_list import EVENT_LIST 
from collections import defaultdict
import matplotlib.pyplot as plt

metrics = {
    "Precision": 0, 
    "Precision(visible)": 1, 
    "Precision(off-screen)": 2, 
    "Recall": 3, 
    "Recall(visible)": 4, 
    "Recall(off-screen)": 5, 
    "F1": 6, 
    "F1(visible)": 7, 
    "F1(Off-screen)": 8,
    "tp": 9,
    "tp_visible": 10,
    "tp_unshown": 11,
    "fp": 12,
    "fp_visible": 13,
    "fp_unshown": 14,
    "fn": 15,
    "fn_visible": 16,
    "fn_unshown": 17
}

def create_highest_scores(data): #returns a array: #9 x 17: Rows: Metrics (f1, f1_visible, f1_unshown, precision, precision_unshown...) col: classes
    #Getting for F1(all):
    index_overview = np.zeros((17, 3)) #rows: classes, cols: f1_index, f1_visible_index, f1_unshown_index
    for i in range(6, 9):
        j = i - 6
        m = data[i]
        for c in range(17):
            highest_threshold_i = np.argsort(m[:,c])[-1]

            index_overview[c][j] = highest_threshold_i

    scores = np.zeros((9, 17))#9 x 17: Rows: Metrics (f1, f1_visible, f1_unshown, precision, precision_unshown...) col: classes
    for i in range(0, 9):
        curr_data = data[i]
        for c in range(17):
            if i in [0, 3, 6]: #all
                scores[i][c] = curr_data[int(index_overview[c][0])][c]
            elif i in [1, 4, 7]: #visible
                scores[i][c] = curr_data[int(index_overview[c][1])][c]
            else: #unshown
                scores[i][c] = curr_data[int(index_overview[c][2])][c]
    return scores

def create_barplot(baseline_scores, ex_scores, metric):
    filename = "barplot_comparison_lgc_60_{}.png".format(metric)
    X = EVENT_LIST
    Y_baseline = baseline_scores[metrics[metric]]
    Y_ex = ex_scores[metrics[metric]]

    X_axis = np.arange(len(X))

    plt.bar(X_axis - 0.2, Y_baseline, 0.4, label = "Baseline")
    plt.bar(X_axis + 0.2, Y_ex, 0.4, label = "Our model")

    plt.xticks(X_axis, X, rotation=90)
    plt.xlabel("Class")
    plt.ylabel("Score")
    plt.title("{}:".format(metric))
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()

def create_table_for_barplot(baseline_scores, ex_scores, metric):
    template_table_start = """
    \\begin{table}[h!bt]
    \\centering
    \\footnotesize
    \\makebox[\\textwidth][c]{
    \\begin{tabularx}{552pt}{|c|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|}
    \\toprule
    Model & \\rotatebox{90}{Ball out of play} & \\rotatebox{90}{Throw-in} & \\rotatebox{90}{Foul} & \\rotatebox{90}{Ind. free-kick} & \\rotatebox{90}{Clearance} & \\rotatebox{90}{Shots on tar.} & \\rotatebox{90}{Shots off tar.} & \\rotatebox{90}{Corner} & \\rotatebox{90}{Substitution} & \\rotatebox{90}{Kick-off} & \\rotatebox{90}{Yellow card} & \\rotatebox{90}{Offside} & \\rotatebox{90}{Dir. free-kick} & \\rotatebox{90}{Goal} & \\rotatebox{90}{Penalty} & \\rotatebox{90}{Yel. to Red} & \\rotatebox{90}{Red card} \\\\
    \\midrule
    """
    template_table_end = """
    \\bottomrule
    \\end{tabularx}
    }
    \\caption{CAPTION HERE}
    \\label{table:f1_score_per_class_baseline}
    \\end{table}
    """
    data_string = """"""
    """    Our model & 0.38 & 0.24 & 0.16 & 0.15 & 0.11 & 0.08 & 0.07 & 0.07 & 0.04 & 0.04 & 0.03 & 0.03 & 0.03 & 0.02 & 0.00 & 0.00 & 0.00 \\\\
        Baseline & 0.56 & 0.52 & 0.36 & 0.37 & 0.36 & 0.36 & 0.44 & 0.45 & 0.57 & 0.32 & 0.33 & 0.25 & 0.26 & 0.31 & 0.44 & 0.00 & 0.27 \\\\"""

    data_string += "Our model & "
    for i, score in enumerate(ex_scores[metrics[metric]]):
        if i == len(ex_scores[metrics[metric]]) - 1:
            data_string += "{} \\\\\n".format(round(score, 2))
        else:
            data_string += "{} & ".format(round(score, 2))

    data_string += "Baseline & "
    for i, score in enumerate(baseline_scores[metrics[metric]]):
        if i == len(baseline_scores[metrics[metric]]) - 1:
            data_string += "{} \\\\\n".format(round(score, 2))
        else:
            data_string += "{} & ".format(round(score, 2))

    table = template_table_start + data_string + template_table_end

    table_string = "-----------------TABLE FOR: {} -----------------\n\n".format(metric) + table
    return table_string

def get_summary_scores(model_data, model_name):
    #Getting for F1(all):
    index_overview = np.zeros((17, 3)) #rows: classes, cols: f1_index, f1_visible_index, f1_unshown_index
    for i in range(6, 9):
        j = i - 6
        m = model_data[i]
        for c in range(17):
            highest_threshold_i = np.argsort(m[:,c])[-1]
            highest_threshold = round(highest_threshold_i * 0.005, 2)
            highest_threshold_score = m[highest_threshold_i, c]

            index_overview[c][j] = highest_threshold_i
        total_TP = 0
        total_TP_visible = 0
        total_TP_unshown = 0
        total_FP = 0
        total_FP_visible = 0
        total_FP_unshown = 0
        total_FN = 0
        total_FN_visible = 0
        total_FN_unshown = 0
    for i in range(9, 18):
        curr_data = model_data[i]
        for c in range(17):
            if i == 9:
                best_i = int(index_overview[c][0])
                total_TP += curr_data[best_i][c]
            elif i == 10:
                best_i = int(index_overview[c][1])
                total_TP_visible += curr_data[best_i][c]
            elif i == 11:
                best_i = int(index_overview[c][2])
                total_TP_unshown += curr_data[best_i][c]
            elif i == 12:
                best_i = int(index_overview[c][0])
                total_FP += curr_data[best_i][c]
            elif i == 13:
                best_i = int(index_overview[c][1])
                total_FP_visible += curr_data[best_i][c]
            elif i == 14:
                best_i = int(index_overview[c][2])
                total_FP_unshown += curr_data[best_i][c]
            elif i == 15:
                best_i = int(index_overview[c][0])
                total_FN += curr_data[best_i][c]
            elif i == 16:
                best_i = int(index_overview[c][1])
                total_FN_visible += curr_data[best_i][c]
            else:
                best_i = int(index_overview[c][2])
                total_FN_unshown += curr_data[best_i][c]

    precision_total = round(total_TP / (total_TP + total_FP), 2)
    precision_visible = round(total_TP_visible / (total_TP_visible + total_FP_visible), 2)
    precision_unshown = round(total_TP_unshown / (total_TP_unshown + total_FP_unshown), 2)
    recall_total = round(total_TP / (total_TP + total_FN), 2)
    recall_visible =  round(total_TP_visible / (total_TP_visible + total_FN_visible), 2)
    recall_unshown = round(total_TP_unshown / (total_TP_unshown + total_FN_unshown), 2)
    f1_total = round(2 * ((precision_total * recall_total) / (precision_total + recall_total)), 2)
    f1_visible = round(2 * ((precision_visible * recall_visible) / (precision_visible + recall_visible)), 2)
    f1_unshown = round(2 * ((precision_unshown * recall_unshown) / (precision_unshown + recall_unshown)), 2)
    print("--------------- TABLE FOR TOTAL SCORES ({})----------------".format(model_name))
    print("TP: {}".format(total_TP))
    print("TP(Visible) {}".format(total_TP_visible))
    print("TP(unshown): {}".format(total_TP_unshown))
    print("FP: {}".format(total_FP))
    print("FP(Visible) {}".format(total_FP_visible))
    print("FP(unshown): {}".format(total_FP_unshown))
    print("FN: {}".format(total_FN))
    print("FN(Visible) {}".format(total_FN_visible))
    print("FN(unshown): {}".format(total_FN_unshown))
    print("PRECISION: {}".format(precision_total))
    print("PRECISION (Visible): {}".format(precision_visible))
    print("PRECISION (unshown): {}".format(precision_unshown))
    print("RECALL: {}".format(recall_total))
    print("RECALL(VISIBLE): {}".format(recall_visible))
    print("RECALL (unshown): {}".format(recall_unshown))
    print("F1: {}".format(f1_total))
    print("F1(visible): {}".format(f1_visible))
    print("F1(unshown): {}".format(f1_unshown))

def get_table_optimal_confidence_thresholds_for_model(baseline_data, ex_data):
    template_table_start = """
    \\begin{table}[h!bt]
    \\centering
    \\footnotesize
    \\makebox[\\textwidth][c]{
    \\begin{tabularx}{552pt}{|c|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|}
    \\toprule
    Threshold & \\rotatebox{90}{Ball out of play} & \\rotatebox{90}{Throw-in} & \\rotatebox{90}{Foul} & \\rotatebox{90}{Ind. free-kick} & \\rotatebox{90}{Clearance} & \\rotatebox{90}{Shots on tar.} & \\rotatebox{90}{Shots off tar.} & \\rotatebox{90}{Corner} & \\rotatebox{90}{Substitution} & \\rotatebox{90}{Kick-off} & \\rotatebox{90}{Yellow card} & \\rotatebox{90}{Offside} & \\rotatebox{90}{Dir. free-kick} & \\rotatebox{90}{Goal} & \\rotatebox{90}{Penalty} & \\rotatebox{90}{Yel. to Red} & \\rotatebox{90}{Red card} \\\\
    \\midrule
    """
    template_table_end = """
    \\bottomrule
    \\end{tabularx}
    }
    \\caption{CAPTION HERE}
    \\label{table:f1_score_per_class_baseline}
    \\end{table}
    """
    #BASELINE:
    index_overview_baseline = np.zeros((17, 3)) #rows: classes, cols: f1_index, f1_visible_index, f1_unshown_index
    for i in range(6, 9):
        j = i - 6
        m = baseline_data[i]
        for c in range(17):
            highest_threshold_i = np.argsort(m[:,c])[-1]
            index_overview_baseline[c][j] = highest_threshold_i
    #OUR MODEL:
    index_overview_ex = np.zeros((17, 3)) #rows: classes, cols: f1_index, f1_visible_index, f1_unshown_index
    for i in range(6, 9):
        j = i - 6
        m = ex_data[i]
        for c in range(17):
            highest_threshold_i = np.argsort(m[:,c])[-1]
            index_overview_ex[c][j] = highest_threshold_i

    table_string = """"""
    threshold_category = ["all", "visible", "off-screen"]
    for s in range(0, 3):
        table_string += "{} & & & & & & & & & & & & & & & & &\\\\\n".format(threshold_category[s])
        thresholds_baseline = index_overview_baseline[:,s]
        thresholds_ex = index_overview_ex[:, s]
        table_string += "Baseline & ".format(threshold_category[s])
        for i, t_b in enumerate(thresholds_baseline):
            if i == len(thresholds_baseline) - 1:
                table_string += "{}\\\\\n".format(round(t_b * 0.005, 2))
                table_string += "Our model & ".format(threshold_category[s])
                for i, t_ex in enumerate(thresholds_ex):
                    if i == len(thresholds_ex) - 1:
                        table_string += "{}\\\\\n".format(round(t_ex * 0.005, 2))
                    else:
                        table_string += "{} & ".format(round(t_ex * 0.005, 2))
            else:
                table_string += "{} & ".format(round(t_b * 0.005, 2))
    print("TABLE OF OPTIMAL CONFIDENCE THRESHOLDS FOR BASELINE/OUR MODEL:")
    print(template_table_start + table_string + template_table_end)


def get_stats_classwise(model_data):
    #Getting for F1(all):
    index_overview = np.zeros((17, 3)) #rows: classes, cols: f1_index, f1_visible_index, f1_unshown_index
    for i in range(6, 9):
        j = i - 6
        m = model_data[i]
        for c in range(17):
            highest_threshold_i = np.argsort(m[:,c])[-1]

            index_overview[c][j] = highest_threshold_i
    
    for m in range(9, 18):
        if m in [9, 12, 15]:
            confidence_i = int(index_overview[c][0])
        elif m in [10, 13, 16]:
            confidence_i = int(index_overview[c][1])
        else:
            confidence_i = int(index_overview[c][2])
        for c in range(0, 17):
            print("{} for class: {}: {}".format(list(metrics.keys())[m], EVENT_LIST[c], model_data[m][confidence_i][c]))

def create_classwise_stats_table(model_data, model_name):
    template_table_start = """
    \\begin{table}[h!bt]
    \\centering
    \\footnotesize
    \\makebox[\\textwidth][c]{
    \\begin{tabularx}{520pt}{|c|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|}
    \\toprule
    Metric & \\rotatebox{90}{Ball out of play} & \\rotatebox{90}{Throw-in} & \\rotatebox{90}{Foul} & \\rotatebox{90}{Ind. free-kick} & \\rotatebox{90}{Clearance} & \\rotatebox{90}{Shots on tar.} & \\rotatebox{90}{Shots off tar.} & \\rotatebox{90}{Corner} & \\rotatebox{90}{Substitution} & \\rotatebox{90}{Kick-off} & \\rotatebox{90}{Yellow card} & \\rotatebox{90}{Offside} & \\rotatebox{90}{Dir. free-kick} & \\rotatebox{90}{Goal} & \\rotatebox{90}{Penalty} & \\rotatebox{90}{Yel. to Red} & \\rotatebox{90}{Red card} \\\\
    \\midrule
    """
    template_table_end = """
    \\bottomrule
    \\end{tabularx}
    }
    \\caption{CAPTION HERE}
    \\label{table:f1_score_per_class_baseline}
    \\end{table}
    """

    index_overview = np.zeros((17, 3)) #rows: classes, cols: f1_index, f1_visible_index, f1_unshown_index
    for i in range(6, 9):
        j = i - 6
        m = model_data[i]
        for c in range(17):
            highest_threshold_i = np.argsort(m[:,c])[-1]
            index_overview[c][j] = highest_threshold_i
    visibility = ""
    metric = ""
    table_string = """"""
    for m in range(9, 18):
        if m in [9, 12, 15]:
            confidence_i = int(index_overview[c][0])
            metric = "TP"
        elif m in [10, 13, 16]:
            confidence_i = int(index_overview[c][1])
            metric = "FP"
        else:
            confidence_i = int(index_overview[c][2])
            metric = "FN"
        if m == 9:
            visibility = "All"
        elif m == 12:
            visibility = "Visible"
        else:
            visibility = "Off-screen"
        if m in [9, 12, 15]:
            table_string += "{} & & & & & & & & & & & & & & & & &\\\\\n".format(visibility)
        table_string += "{} & ".format(metric)
        for c in range(0, 17):
            if m in [9, 12, 15]:
                confidence_i = int(index_overview[c][0])
            elif m in [10, 13, 16]:
                confidence_i = int(index_overview[c][1])
            else:
                confidence_i = int(index_overview[c][2])
        
            if c < 16:
                table_string += "{} & ".format(int(model_data[m][confidence_i][c]))
            else:
                table_string += "{} \\\\\n".format(int(model_data[m][confidence_i][c]))
            #print("{} for class: {}: {}".format(list(metrics.keys())[m], EVENT_LIST[c], model_data[m][confidence_i][c]))
    table = template_table_start + table_string + template_table_end
    print("============STATS-TABLE FOR: {}============".format(model_name))
    print(table)


data_our_model = np.load("/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/brynjard/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_our_model_delta_60.npy")
data_baseline = np.load("/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/brynjard/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_baseline_delta_60.npy")
print(data_baseline.shape)
"""
baseline_scores = create_highest_scores(data)
get_summary_scores(data, "baseline")

ex_scores = create_highest_scores(data)
get_summary_scores(data, "Our model")"""
#get_table_optimal_confidence_thresholds_for_model(data_baseline, data_our_model)
#print("STATS FOR BASELINE:")
#get_stats_classwise(data_baseline)
#print("STATS FOR OUR MODEL: ")
#get_stats_classwise(data_our_model)
#for m in range(0, 9):  
    #create_barplot(baseline_scores, ex_scores, list(metrics.keys())[m])
    #print(create_table_for_barplot(baseline_scores, ex_scores, list(metrics.keys())[m]))

create_classwise_stats_table(data_baseline, "baseline")
create_classwise_stats_table(data_our_model, "our Model")
    














