from turtle import title
import matplotlib.pyplot as plt
import numpy as np
from event_list import EVENT_LIST

def create_barplot(baseline_scores, experiment_scores, chart_title):
    filename = f"barchart_{chart_title}.png"
    X = EVENT_LIST
    
    Y_baseline = baseline_scores['data']
    baseline_label = baseline_scores['label']
    Y_ex = experiment_scores['data']
    experiment_label = experiment_scores['label']

    X_axis = np.arange(len(X))

    plt.bar(X_axis - 0.2, Y_baseline, 0.4, label=baseline_label)
    plt.bar(X_axis + 0.2, Y_ex, 0.4, label=experiment_label)

    plt.xticks(X_axis, X, rotation=90)
    plt.xlabel("Class")
    plt.ylabel("Average-mAP")
    plt.title(f"{chart_title}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()


if __name__ == '__main__':
    ## Read csv file

    experiment_scores = {
                        "label": "Experiment 1",
                        "data": [83.3,78.8,73.0,76.7,40.8,39.5,40.9,69.8,70.7,73.5,65.0,42.7,66.1,79.5,61.2,25.6,22.8]
                        }
    baseline_score = {
                        "label": "Baseline",
                        "data": [86.1,73.1,73.5,76.2,40.2,38.7,40.9,69.3,70.6,72.1,64.6,39.6,65.1,80.6,60.8,25.1,30.7]
                        }
    
    chart_title = "Experiment 1"
    create_barplot(experiment_scores, baseline_score, chart_title)