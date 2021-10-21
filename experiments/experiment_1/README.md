## Experiment #1: Train NETVLAD++ on visible events only.
---
- Our goal is to combine 3 classifiers (current, next, previous).  
 We will try to make our current classifier perform better by only training on visible events.

- Performance metric: Average mAP on visible events only.  
Can compare with the *Shown only* metric on the [SoccerNet Challenge](https://eval.ai/web/challenges/challenge-page/761/leaderboard/2074#leaderboardrank-7)  

- We use NetVLAD++, but modify the *SoccerNetClips* class in *dataset.py* in order to ignore the annotions that has the  *visibility* attribute set to *not shown*. We will use the Baidu features.
- Original [repo](https://github.com/SilvioGiancola/SoccerNetv2-DevKit/tree/main/Task1-ActionSpotting/TemporallyAwarePooling)
