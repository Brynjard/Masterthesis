## Experiment #2: Training a next and previous model by swapping labels. 
---
- We train two models (previous, next) by swapping the labels in the training data. 	For a given event, our next-model will learn the event following it, and our previous model will be taught the event preceding it. 

-  Performance metric: Average mAP on test-data. 

- We use NetVLAD++ since the model is a part of the SoccerNetv2 dev-kit and therefore ready-to-use. The different features can be utilized with an command line argument.
- Original repo link: https://github.com/SilvioGiancola/SoccerNetv2-DevKit/tree/main/Task1-ActionSpotting/TemporallyAwarePooling