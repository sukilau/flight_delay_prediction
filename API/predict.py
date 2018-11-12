import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, Imputer, StandardScaler, RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.neural_network import MLPClassifier
import PipelineHelper

def predict_flight_delay(x, modelfile="model.pkl"):
    pickle_model = pickle.load(open(modelfile, 'rb'))
    x = pd.DataFrame(x, columns=['AIRLINE','DAY_OF_WEEK', 'MONTH', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT'])
    
    print(x)
    print(x['DAY_OF_WEEK'])
    print(x['MONTH'])
    y = pickle_model.predict(x)[0]
    prob = pickle_model.predict_proba(x)[0][y]
    print('Predicted label = {} with probability {:.2f}'.format(y, prob))
    return  y, prob

