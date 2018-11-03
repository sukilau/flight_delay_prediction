# import numpy as np
# import pandas as pd
# import pickle
# from sklearn.base import BaseEstimator, TransformerMixin
# from sklearn.preprocessing import Imputer, StandardScaler, LabelEncoder, LabelBinarizer
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning) 
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, Imputer, StandardScaler, RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

def predict_flight_delay(x=[['DL',7,1424.0,1035]], modelfile="../model/model.pkl"):

    with open(modelfile, 'rb') as file:  
        pickle_model = pickle.load(file)

    x = pd.DataFrame(data, columns=['AIRLINE','DAY_OF_WEEK','DEPARTURE_TIME','DISTANCE'])
    y_pred = pickle_model.predict(x)
    print("DEBUG")
    print(y_pred[0])
    return y_pred[0]

#     if y_pred[0] > 0.5:
#         print('Predicted gender : Female with prob', y_pred[0])
#         y_gender = 'female'
#         y_prob = y_pred[0]
#     else:
#         print('Predicted gender : Male with prob', 1-y_pred[0])
#         y_gender = 'male'
#         y_prob = 1-y_pred[0]

#     return y_gender, y_prob 

        
if __name__ == "__main__":
    predict_flight_delay()
