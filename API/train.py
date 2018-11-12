import pandas as pd
import numpy as np
import pickle
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from PipelineHelper import *


seed = 200    
    
def define_pipeline(categorical_features, estimator):
    '''Define ML pipeline for general ML problem of mixed numerical and categorical features'''
    cat_pipe = []
    for col in categorical_features:
        cat_pipe.append((col, make_pipeline(ItemSelector(key=col), CustomLabelBinarizer())))
        
    pipe = Pipeline([
        ('feature_union', FeatureUnion(cat_pipe)),
        ('estimator', estimator)
    ])
    return pipe


def descretize(x, cutoff1, cutoff2):
    '''Convert numeric values of x to multiclass label'''
    if x < cutoff1:
        return 0
    elif x < cutoff2:
        return 1
    else: 
        return 2
    
    
def main():
    # load data
    df = pd.read_csv("data/flights.csv", low_memory=False)
#     df = df.sample(frac=0.001, random_state=0)

    # remove data rows with origin/destination airport in digit code
    df['origin_airport_isdigit'] = [x.isdigit() for x in df['ORIGIN_AIRPORT']]
    df['destination_airport_isdigit'] = [x.isdigit() for x in df['DESTINATION_AIRPORT']]
    df = df[(df['origin_airport_isdigit']==False) & (df['destination_airport_isdigit']==False)]

    # define features
    categorical_features = ['AIRLINE','DAY_OF_WEEK', 'MONTH', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']
    df = df[categorical_features + ['ARRIVAL_DELAY']]

    # drop data rows with any null value
    df.dropna(inplace=True)

    # create multi-class label
    df['label'] = df['ARRIVAL_DELAY'].map(lambda x: descretize(x, 0, 30))

    X = df[categorical_features]
    y = df['label']

    # define pipeline
    estimator = MLPClassifier(hidden_layer_sizes=(32,64,16), activation='relu', solver='adam', 
                             max_iter=100, early_stopping=False, random_state=0)
    pipe = define_pipeline(categorical_features, estimator)

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.3)

    # fit pipeline
    pipe.fit(X_train, y_train)

    # save model
    pickle.dump(pipe, open('model.pkl', 'wb'))


if __name__ == "__main__":
    main()


