from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

import datafusion_utils as utils
from event_list import EVENT_LIST

SUB_EVENT_LIST = ""

def create_plot(tp_differences, fp_differences, fn_differences):
    filename = "percentage_diff_barplot.png"
    X = EVENT_LIST

    X_axis = np.arange(len(X))
    step = 4
    X_axis = np.array([i for i in range(0, 17*step, step)])
    print(X_axis)

    width = 1

    plt.bar(X_axis - 1, tp_differences, width, label = "True positive")
    plt.bar(X_axis, fp_differences, width, label = "False positive")
    plt.bar(X_axis + 1, fn_differences, width, label = "False negative")

    plt.xticks(X_axis, X, rotation=90)
    plt.xlabel("Class")
    plt.ylabel("Percentage difference")
    plt.title("Differences in percentage")
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()

def create_plot_from_dict(difference_dict):
    """
        difference_dict has the following format:

        {
            "Ball out of play": [-3.12, 13.93, 6.67],
            "Throw in": [-13.53, 39.55, 14.2],
            ...
        }

        In the the list contains [true_positive_difference, false_positive_difference, false_negative_difference]

    """
    fig, ax = plt.subplots()
    width = 0.5
    x_axis_values = np.array([0.0, 0.6, 1.2])

    # for key, value in difference_dict.items():
    #     class_bars = ax.bar(x_axis_values, value, width, label=key)
    #     x_axis_values += 3

    tp_differences = difference_dict["tp"]
    fp_differences = difference_dict["fp"]
    fn_differences = difference_dict["fn"]
    
    filename = "percentage_diff_barplot_small.png"

    x_labels = list(difference_dict.keys())

    # x_axis_values = np.arange(len(x_labels))
    # step = 4
    # x_axis_values = np.array([i for i in range(0, 17*step, step)])

    # width = 1

    plt.bar(x_axis_values - 1, tp_differences, width, label = "True positive")
    plt.bar(x_axis_values, fp_differences, width, label = "False positive")
    plt.bar(x_axis_values + 1, fn_differences, width, label = "False negative")

    # plt.xticks(x_axis_values, x_labels, rotation=90)
    plt.xlabel("Class")
    plt.ylabel("Percentage difference")
    plt.title("Differences in percentage")
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()


def create_plot_with_subclasses(labels, differences):
    filename = "relative_difference_percentage_barplot.png"
    X = labels

    # X_axis = np.arange(len(X))
    step = 6
    X_axis = np.array([i for i in range(0, len(labels)*step, step)])

    width = 1
    
    plt.grid(zorder=0)

    plt.bar(X_axis - 1, differences[0], width, label = "True positive", zorder=3)
    plt.bar(X_axis, differences[1], width, label = "False positive", zorder=3)
    plt.bar(X_axis + 1, differences[2], width, label = "False negative", zorder=3)
    
    plt.axhline(y=0.0, color='black', linewidth=1)

    plt.xticks(X_axis, X, rotation=90)

    y_ticks = [i for i in range(-85, 80, 10)]
    plt.ylim([-85, 85])

    # plt.yticks(y_ticks)
    
    # fig, ax = plt.subplots()
    ax = plt.gca()
    ax.set_axisbelow(True)
    # ax.set_major_locator(MultipleLocator(20))
    # ax.set_major_formatter(FormatStrFormatter('%d'))

    # # For the minor ticks, use no labels; default NullFormatter.
    # ax.YAxis.set_minor_locator(MultipleLocator(10))

    plt.xlabel("Class")
    plt.ylabel("Relative difference in %")
    plt.title("Relative difference in outcomes between our model and baseline")
    plt.legend(loc='upper center', ncol=3)
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()


def create_diff_dict(listOfLists):
    print(listOfLists)
    difference_dict = dict()
    for i, e in enumerate(EVENT_LIST):
        class_slice = listOfLists[:,i]
        result = np.all(class_slice == [0, 0, 0])
        if not result:
            difference_dict[e] = class_slice
        # print(result)
        # print(class_slice)
        # exit()
    return difference_dict

def remove_classes_with_no_difference(listOfLists):
    labels = list()
    tp = list()
    fp = list()
    fn = list()

    for i, e in enumerate(EVENT_LIST):
        class_slice = listOfLists[:,i]
        result = np.all(class_slice == [0, 0, 0])
        if not result:
            labels.append(e)
            tp.append(listOfLists[0,i])
            fp.append(listOfLists[1,i])
            fn.append(listOfLists[2,i])
        # print(result)
        # print(class_slice)
        # exit()
    return labels, np.array([tp, fp, fn])
        


def format_with_two_decimal_points(value):

    value = str(round(value, 2))
    decimal_part = value.split(".")[1]
    
    if len(decimal_part) != 2:
        value = value.split(".")[0] + "." + decimal_part + "0"
    
    return value

if __name__ == '__main__':

    tp_our_model = "192 & 547 & 20 & 628 & 383 & 0 & 0 & 72 & 27 & 219 & 4 & 6 & 0 & 0 & 0 & 0 & 0"
    tp_our_model = tp_our_model.split(" & ")
    tp_our_model = [int(x) for x in tp_our_model]
    tp_baseline = "198 & 621 & 11 & 669 & 456 & 0 & 0 & 79 & 27 & 172 & 4 & 5 & 0 & 0 & 0 & 0 & 0"
    tp_baseline = tp_baseline.split(" & ")
    tp_baseline = [int(x) for x in tp_baseline]
    print(tp_baseline)

    tp_differences_str = ["0.00" if tp_our_model[i] == 0 else format_with_two_decimal_points((tp_our_model[i] - tp_baseline[i])/tp_our_model[i] * 100) for i in range(len(tp_our_model))]
    tp_differences = [float(x) for x in tp_differences_str]
    print(tp_differences)

    fp_our_model = "122 & 574 & 12 & 867 & 435 & 14 & 10 & 10 & 24 & 155 & 18 & 34 & 56 & 8 & 3 & 44 & 18"
    fp_our_model = fp_our_model.split(" & ")
    fp_our_model = [int(x) for x in fp_our_model]
    fp_baseline = "105 & 347 & 5 & 783 & 512 & 14 & 10 & 18 & 24 & 79 & 28 & 27 & 56 & 8 & 3 & 44 & 18"
    fp_baseline = fp_baseline.split(" & ")
    fp_baseline = [int(x) for x in fp_baseline]

    fp_differences_str = ["0.00" if fp_our_model[i] == 0 else format_with_two_decimal_points((fp_our_model[i] - fp_baseline[i])/fp_our_model[i] * 100) for i in range(len(fp_our_model))]
    fp_differences = [float(x) for x in fp_differences_str]
    print(fp_differences)

    fn_our_model = "90 & 521 & 20 & 389 & 470 & 1 & 2 & 46 & 65 & 138 & 27 & 15 & 17 & 0 & 0 & 0 & 0"
    fn_our_model = fn_our_model.split(" & ")
    fn_our_model = [int(x) for x in fn_our_model]
    fn_baseline = "84 & 447 & 29 & 348 & 397 & 1 & 2 & 39 & 65 & 185 & 27 & 16 & 17 & 0 & 0 & 0 & 0"
    fn_baseline = fn_baseline.split(" & ")
    fn_baseline = [int(x) for x in fn_baseline]

    fn_differences_str = ["0.00" if fn_our_model[i] == 0 else format_with_two_decimal_points((fn_our_model[i] - fn_baseline[i])/fn_our_model[i] * 100) for i in range(len(fn_our_model))]
    fn_differences = [float(x) for x in fn_differences_str]
    print(fn_differences)

    diff_dict = create_diff_dict(np.array([tp_differences, fp_differences, fn_differences]))

    create_plot(tp_differences=tp_differences, fp_differences=fp_differences, fn_differences=fn_differences)

    # create_plot_from_dict(diff_dict)


    labels, listOfLists = remove_classes_with_no_difference(np.array([tp_differences, fp_differences, fn_differences]))
    create_plot_with_subclasses(labels, listOfLists)

