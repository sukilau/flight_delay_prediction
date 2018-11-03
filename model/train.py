import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, Imputer, StandardScaler, RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

unseen_label = "__New__"
seed = 200

class CustomLabelBinarizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.le = LabelEncoder()
        self.lb = LabelBinarizer()
        self.seen_labels = set()
        
    def fit(self, x, y=None,**fit_params):
        self.seen_labels = set(x)
        self.seen_labels.add(unseen_label)
        
        # add "unseen" to X
        x_new = list(x)
        x_new.append(unseen_label)

        label_encoded = self.le.fit_transform(x_new)
        self.lb.fit(label_encoded)
        return self
    
    def transform(self, x):
        x_new = list(map(lambda label: label if label in self.seen_labels else unseen_label, list(x)))
        label_encoded = self.le.transform(x_new)
        return self.lb.transform(label_encoded)
    

class ItemSelector(BaseEstimator, TransformerMixin):
    '''Select a column of data by a provided key'''
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, df):
        return df[self.key]

    
class MultiItemSelector(BaseEstimator, TransformerMixin):
    '''Select multiple columns of data by a provided list of keys'''
    def __init__(self, key_list):
        self.key_list = key_list

    def fit(self, x, y=None):
        return self

    def transform(self, df):
        return df[self.key_list]
    
    
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
    
    import os
    cwd = os.getcwd()
    print(cwd)

    # load data
    df = pd.read_csv("data/flights.csv", low_memory=False)
    df = df.sample(frac=0.1, random_state=0)
    
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
    estimator = RandomForestClassifier(n_estimators=3, max_depth=3, n_jobs=-1, random_state=0)
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


