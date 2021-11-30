from ift6758.data.milestone2.question_3_angle import angle_feature
from ift6758.data.milestone2.question_3_distance import distance_feature
from ift6758.data.milestone2.question_3_dist_ang import angle_distance_feature
from ift6758.data.milestone2.question_3_random_baseline import random_baseline
from ift6758.data.milestone2.question_2 import Featurizer
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


''' decommentez et executer la ligne qui suit si vous n'avez pas encore les donner au format pkl'''
dataformodelpath = os.path.dirname('/Users/macbook/Documents/GitHub/IFT6758_Milestone-1/ift6758-project-template-main/ift6758/features')+"/data_for_models"
#ftz = Featurizer(2015, 2019)
#features_df = ftz.get_feature()
#features_df.to_pickle(dataformodelpath + "/features_df.pkl")

features_df = pd.read_pickle(os.path.dirname('/Users/macbook/Documents/GitHub/IFT6758_Milestone-1/ift6758-project-template-main/ift6758/features') + "/data_for_models/features_df.pkl")

random_baseline(features_df)
distance_feature(features_df)
angle_feature(features_df)
angle_distance_feature(features_df)
plt.show()