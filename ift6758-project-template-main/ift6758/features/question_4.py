from ift6758.data.question_4 import *
from ift6758.data.question_6 import HeatMapShots
pd.set_option("display.max_columns", 100)
from sklearn import preprocessing
from sklearn import feature_extraction



X_NET_COORDINATE = 10

def load_data(year):
    tidyer = Tidyer()
    shots_and_goals = tidyer.game_event_to_panda_df(year)
    other_events = tidyer.other_events_to_panda_df(year)
    return shots_and_goals, other_events

def prepare_data_for_feature_engineering(shots_and_goals, other_events):

    season_data = pd.concat([shots_and_goals["regular"], other_events["regular"]])
    season_data = season_data.sort_values(by=["game_id", "which_period", "period_time"])
    season_data = calculate_distance_from_net(season_data)
    season_data = calculate_angle(season_data)
    season_data = convert_time_to_game_seconde(season_data)
    season_data = join_preceding_events(season_data)
    season_data = calculate_distance_from_last_event(season_data)
    season_data.loc[:,"empty_net"] = season_data.goalie_name.isna()
    season_data.loc[:,"time_since_last_event"] = season_data.game_seconds - season_data.pre_game_seconds
    season_data.loc[:,"rebound"] = season_data.pre_event_type == "Shot"
    season_data.loc[:,"change_in_shot_angle"] = np.abs(season_data.angle_from_net - season_data.pre_angle_from_net)
    season_data.loc[season_data.rebound == False,"change_in_shot_angle"] = None
    season_data.loc[season_data.time_since_last_event == 0,"time_since_last_event"] = 1
    season_data["speed"] = season_data.distance_from_last_event / season_data.time_since_last_event
    return season_data

def calculate_distance_from_net(season_data):
    heatmap_function = HeatMapShots(2017)
    season_data = heatmap_function.rearange_coordinates(season_data)
    season_data["distance_from_net"] = np.sqrt((season_data.coord_x - X_NET_COORDINATE) ** 2 + season_data.coord_y ** 2)
    return season_data

def calculate_angle(season_data):
    season_data.loc[:, "angle_from_net"] = np.arccos(
        (season_data.coord_x - X_NET_COORDINATE) / season_data.distance_from_net)
    season_data.loc[season_data.coord_y < 0, "angle_from_net"] = -season_data.loc[season_data.coord_y < 0,
                                                                                  "angle_from_net"]
    return season_data

def join_preceding_events(season_data):
    preceding_event = create_preceding_event_table(season_data)

    season_data = season_data.reset_index()
    preceding_event = preceding_event.reset_index()
    season_data = season_data.join(preceding_event.iloc[:, [i for i in range(1, 7)]])
    season_data = season_data[season_data.event_type.isin(["Shot", "Goal"])]
    return season_data

def create_preceding_event_table(season_data):
    preceding_event = season_data.loc[:, ["game_seconds", "which_period", "event_type", "coord_x", "coord_y", "angle_from_net"]]
    preceding_event = preceding_event.iloc[:(preceding_event.shape[0] - 1), ]
    dump_row = {"game_seconds": [None], "which_period": [None], "event_type": [None], "coord_x": [None],
                "coord_y": [None], "angle_from_net" : [None]}
    dump_row = pd.DataFrame(dump_row)
    preceding_event = pd.concat([dump_row, preceding_event])
    preceding_event = preceding_event.rename(columns={"game_seconds": "pre_game_seconds", "which_period": "pre_which_period", "event_type": "pre_event_type",
                 "coord_x": "pre_coord_x", "coord_y": "pre_coord_y", "angle_from_net": "pre_angle_from_net"})
    return  preceding_event


def convert_time_to_game_seconde(season_data):
    seconds_per_minutes = 60
    minutes_per_period = 20
    minutes = season_data.period_time.apply(lambda x: int(x[:2]))
    seconds = season_data.period_time.apply(lambda x: int(x[3:5]))
    period = season_data.which_period

    game_seconds = (period - 1) * minutes_per_period + minutes * seconds_per_minutes + seconds
    season_data.loc[:,"game_seconds"] = game_seconds
    return season_data

def calculate_distance_from_last_event(season_data):
    season_data.loc[:,"distance_from_last_event"] = np.sqrt((season_data.coord_x - season_data.pre_coord_x) ** 2 +
                                                      (season_data.coord_y - season_data.pre_coord_y) ** 2)
    return season_data

def engineer_features(season_data):
    categorial_features = ['which_period', 'event_type', 'shot_type', 'pre_event_type', 'rebound']
    continuous_features = ['game_seconds', 'coord_x', 'coord_y', 'distance_from_net', 'angle_from_net',
                           'pre_coord_x', 'pre_coord_y', 'time_since_last_event', 'distance_from_last_event',
                           'change_in_shot_angle', 'speed']
    engineered_data = pd.DataFrame()
    for feat in continuous_features:
        minmax_scaled_col = preprocessing.minmax_scale(season_data.loc[:, feat])
        engineered_data.loc[:, feat] = minmax_scaled_col

    dv = feature_extraction.DictVectorizer(sparse=False)
    for feat in categorial_features:
        feature_column = season_data[[feat]]
        feature_column.loc[:, feat] = feature_column[feat].astype(str)
        one_hot_features = dv.fit_transform(feature_column.to_dict("index").values())
        number_of_feature_type = feature_column.drop_duplicates().shape[0]
        one_hot_features = pd.DataFrame(one_hot_features,
                                        columns=[feat + "_" + str(i) for i in range(number_of_feature_type)])
        engineered_data = engineered_data.join(one_hot_features)

    return engineered_data

data = pd.DataFrame()
for year in [2016,2017,2018,2019]:
    shots_and_goals, other_events = load_data(year)
    season_data = prepare_data_for_feature_engineering(shots_and_goals, other_events)
    season_data = engineer_features(season_data)
    data = pd.concat([data, season_data])

#dealing with nas
data.loc[data.change_in_shot_angle.isna(), "change_in_shot_angle"] = 0
for col in data.columns:
    median = np.median(data.loc[~data[col].isna(),col])
    data.loc[data[col].isna(),col] = median

data.to_pickle(os.path.dirname(__file__) + "/data_for_models/data.pkl")