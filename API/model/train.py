import pandas as pd
import numpy as np
import pickle
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from model.PipelineHelper import *


seed = 200    
    
def define_pipeline(numerical_features, categorical_features, estimator):
    '''Define ML pipeline for general ML problem of mixed numerical and categorical features'''
    cat_pipe = []
    for col in categorical_features:
        cat_pipe.append((col, make_pipeline(ItemSelector(key=col), CustomLabelBinarizer())))
        
    num_pipe = [("numerical", make_pipeline(MultiItemSelector(key_list=numerical_features), Imputer(strategy="median",axis=0)))]
    
    pipe = Pipeline([
        ('feature_union', FeatureUnion(cat_pipe + num_pipe)),
        ('estimator', estimator)
    ])
    return pipe


def main():
    
    # load data
    df = pd.read_csv("data/flights.csv", low_memory=False)
    #df = df.sample(frac=0.001, random_state=0)
    
    # create label
    df["label"] = (df["ARRIVAL_DELAY"]>10)*1

    # define features
    categorical_features = ['AIRLINE','DAY_OF_WEEK']
    numerical_features = ['DEPARTURE_TIME','DISTANCE']
    
    # train test split
    X = df[categorical_features + numerical_features]
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

    # define pipeline
    estimator = RandomForestClassifier(n_estimators=100, max_depth=None, n_jobs=-1, random_state=0)
    pipe = define_pipeline(numerical_features, categorical_features, estimator)
    
    # train model
    pipe.fit(X_train, y_train)
    pipe.score(X_test, y_test)

    # save model
    pkl_filename = "model/model.pkl"  
    with open(pkl_filename, 'wb') as file:  
        pickle.dump(pipe, file)
        
       
        
if __name__ == "__main__":
    main()


