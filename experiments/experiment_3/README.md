## Experiment #3: Training a next and previous model by swapping labels and only keeping relevant labels for each model.
---
- As we did in ex2, we also here train 3 models (past, current, future).
- We saw that ex2 did not yield that many exciting results, so we introduce some domain-knowledge to the models. 
- We still use our Labels from ex2, but train on only the relevant labels for each model. 
- By relevant we mean this: We have an overview over which events in soccer that can be derived with certainty from the event before (for future model) or the event after (for past model): https://docs.google.com/spreadsheets/d/1f1q-_IXURHBX5GNAd57U5yaSio_xruGnVvkmvVStiBc/edit#gid=0
- We use this to filter out the labels we train our past/future models on. For example, in our future model, we know that a ball-out-of-play cannot be inferred from what happened before it. We therefore exclude all training examples of ball-out-of-play. 

-  Performance metric: Average mAP on test-data. 
- This experiment is based on ex2, the original source-code can be found here: https://github.com/SilvioGiancola/SoccerNetv2-DevKit/tree/main/Task1-ActionSpotting/TemporallyAwarePooling