from ift6758.data.milestone2.question_1 import Featurizer
from sklean import


ftz = Featurizer(2015,2019)
features_df = ftz.get_feature()
print(features_df)
