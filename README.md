# Flight Delay Visualization

## Part 1: API for Flight Delay Prediction

We will separate model training and prediction into two parts:
* Training the model offline 
* Building a REST API for flight delay prediction using the trained model

### Setup
* To set up the enviroment for model training and running Flask App, create a virtual environment in Python 3.6 and install the required Python libraries (see `api/requirements.txt`).

### 2.1 Model Training
* To train the model, run `PYTHONPATH=. python model/train.py` at the `api` directory. The trained model will be saved in the `model` directory for later use.

### 2.2 Prediction
* We will use Flask to build a REST API for prediction using the model trained beforehand. The API is designed to accept an example to be predicted. Each API call triggers the feature engineering and prediction process in the machine learning pipeline. This should be fast enough to ensure a real-time response which gives the prediction result in JSON format. 
* To run Flask App, run `PYTHONPATH=. python app.py` at the `api` directory.
* Now, you can test the API end point using your favourite browser, curl or postman.
* Example query using browser :
`http://localhost:5000/prediction?AIRLINE=DL&DAY_OF_WEEK=7&DEPARTURE_TIME=1424.0&DISTANCE=1035`

```
{"AIRLINE":"DL",
"DAY_OF_WEEK":"7",
"DEPARTURE_TIME":1424.0,
"DISTANCE":1035.0,
"Predicted_Delay":"0",
"Prob":"0.8112436783914437"}
```
The prediction label is 0 which means "no delay" with probability 0.8.


## Part 2: UI for Interactive Visualization

(to be added)


