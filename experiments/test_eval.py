import sys
from alternative_evaluation import evaluate_no_delta


if __name__ == '__main__':
    args = sys.argv

    if len(args) < 3:
        print(f"3 command line arguments expected, {len(args) - 1} found")
        exit()
    elif len(args) == 4:
        confidence_threshold = float(args[3])
    else:
        confidence_threshold = 0.0

    soccer_net_path = args[1]
    predictions_folder = args[2]

    metric_dict = evaluate_no_delta(SoccerNet_path=soccer_net_path, Predictions_path=predictions_folder, confidence_threshold=confidence_threshold)