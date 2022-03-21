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
            highest_threshold = round(highest_threshold_i * 0.005, 2)
            highest_threshold_score = m[highest_threshold_i, c]

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
            data_string += "{} \\\\".format(round(score, 2))
        else:
            data_string += "{} & ".format(round(score, 2))

    data_string += "Baseline & "
    for i, score in enumerate(baseline_scores[metrics[metric]]):
        if i == len(baseline_scores[metrics[metric]]) - 1:
            data_string += "{} \\\\".format(round(score, 2))
        else:
            data_string += "{} & ".format(round(score, 2))

    table = template_table_start + data_string + template_table_end

    print("-----------------TABLE FOR: {} -----------------".format(metric))
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
    precision_total = round(total_TP / (total_TP + total_FP), 2)
    print("PRECISION: {}".format(precision_total))
    precision_visible = round(total_TP_visible / (total_TP_visible + total_FP_visible), 2)
    print("PRECISION (Visible): {}".format(precision_visible))
    precision_unshown = round(total_TP_unshown / (total_TP_unshown + total_FP_unshown), 2)
    print("PRECISION (unshown): {}".format(precision_unshown))
    recall_total = round(total_TP / (total_TP + total_FN), 2)
    print("RECALL: {}".format(recall_total))
    recall_visible =  round(total_TP_visible / (total_TP_visible + total_FN_visible), 2)
    print("RECALL(VISIBLE): {}".format(recall_visible))
    recall_unshown = round(total_TP_unshown / (total_TP_unshown + total_FN_unshown), 2)
    print("RECALL (unshown): {}".format(recall_unshown))
    f1_total = round(2 * ((precision_total * recall_total) / (precision_total + recall_total)), 2)
    print("F1: {}".format(f1_total))
    f1_visible = round(2 * ((precision_visible * recall_visible) / (precision_visible + recall_visible)), 2)
    print("F1(visible): {}".format(f1_visible))
    f1_unshown = round(2 * ((precision_unshown * recall_unshown) / (precision_unshown + recall_unshown)), 2)
    print("F1(unshown): {}".format(f1_unshown))
    


data = np.load("/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/brynjard/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_baseline_delta_60.npy")
baseline_scores = create_highest_scores(data)
#get_summary_scores(data, "baseline")

data = np.load("/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/brynjard/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_our_model_delta_60.npy")
ex_scores = create_highest_scores(data)
#get_summary_scores(data, "Our model")

for m in range(0, 9):  
    create_barplot(baseline_scores, ex_scores, list(metrics.keys())[m])
    print(create_table_for_barplot(baseline_scores, ex_scores, list(metrics.keys())[m]))
    














