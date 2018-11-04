import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, Imputer, StandardScaler, RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import model.PipelineHelper

def predict_flight_delay(x, modelfile="model/model.pkl"):
    with open(modelfile, 'rb') as file:  
        pickle_model = pickle.load(file)
    x = pd.DataFrame(x, columns=['AIRLINE','DAY_OF_WEEK','DEPARTURE_TIME','DISTANCE'])
    y_proba = pickle_model.predict_proba(x)[0]
    print(y_proba)
    if y_proba[0]>0.5:
        y_pred = 0
        y_prob = y_proba[0]
    else:
        y_pred = 1
        y_prob = y_proba[1]
    
    return y_pred, y_prob

