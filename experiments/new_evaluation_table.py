template_table_start = """
\\begin{table}[h!bt]
\\centering
\\makebox[\\textwidth][c]{
\\begin{tabularx}{565pt}{|c|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|c@{\\hspace{3pt}}|}
\\toprule
Confidence \\geq & \\rotatebox{90}{Ball out of play} & \\rotatebox{90}{Throw-in} & \\rotatebox{90}{Foul} & \\rotatebox{90}{Ind. free-kick} & \\rotatebox{90}{Clearance} & \\rotatebox{90}{Shots on tar.} & \\rotatebox{90}{Shots off tar.} & \\rotatebox{90}{Corner} & \\rotatebox{90}{Substitution} & \\rotatebox{90}{Kick-off} & \\rotatebox{90}{Yellow card} & \\rotatebox{90}{Offside} & \\rotatebox{90}{Dir. free-kick} & \\rotatebox{90}{Goal} & \\rotatebox{90}{Penalty} & \\rotatebox{90}{Yel. to Red} &    \\rotatebox{90}{Red card} \\\\
\\midrule
"""

template_table_end = """\\bottomrule
\\end{tabularx}
}
\\caption{CAPTION HERE}
\\label{table:template_label}
\\end{table}"""

def create_table_statistics(model_name, scores):
    """
    Creates a table for our statistics-use case. 
    @model_name: The metric you want a table for. precision/recall/f1 according to how @scores is scores. 
    @scores: A nested dict with metrics for all 17 classes for a model. Expected structure: 
    {
        "precision": {
            "Goal": [0.98, 0.96, ... ],
            "Corner": [0.98, 0.96, ... ],
            ...
        },
        "recall": {
            "Goal": [0.98, 0.96, ... ],
            "Corner": [0.98, 0.96, ... ],
            ...
        },
    """
    data = scores[model_name] #17x10 dict, key = class, value = list of scores for each threshold
    granularity = len(data["Goal"])

    data_string = """"""
    current_threshold = 0
    threshold_tick = 1 / granularity
    for i in range(0, granularity):
        threshold_row = """"""
        threshold_row += str(current_threshold) + " & "
        for j,c in enumerate(data.keys()):
            if j == len(data.keys()) - 1:
                threshold_row += str(data[c][i]) + " \\\\"
            else:
                threshold_row += str(data[c][i]) + " & "
        current_threshold = round(current_threshold + threshold_tick, 2)
        data_string += threshold_row
    table_string = template_table_start + data_string + template_table_end
    return table_string
        
        



if __name__ == '__main__':
    test_dict = {
        "precision": {
            "Goal": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Throw-in": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.12],
            "Ball out of play": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Kick-off": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.12],
            "Indirect free-kick": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Clearance": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.12],
            "Foul": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Corner":[2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.12],
            "Substitution": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Offside": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.12],
            "Direct free-kick": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Yellow card": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.12],
            "Shots on target": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Shots off target": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.12],
            "Goal": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Red card": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.12],
            "Penalty": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Yellow->red card": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.12]
        },
        "recall": {
            "Goal": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Throw-in": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Ball out of play": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Kick-off": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Indirect free-kick": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Clearance": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Foul": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Corner":[2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Substitution": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Offside": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Direct free-kick": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Yellow card": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Shots on target": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Shots off target": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Goal": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Red card": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Penalty": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Yellow->red card": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55]
        },
        "f1": {
            "Goal": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Throw-in": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Ball out of play": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Kick-off": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Indirect free-kick": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Clearance": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Foul": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Corner":[2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Substitution": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Offside": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Direct free-kick": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Yellow card": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Shots on target": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Shots off target": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Goal": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Red card": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Penalty": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55],
            "Yellow->red card": [2.13, 3.13, 2.55, 6.55, 4.33, 4.33, 1.23, 9.55, 3.44, 4.55]
        }
    }
    create_table_statistics("precision", test_dict)