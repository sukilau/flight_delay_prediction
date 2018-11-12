# API for Flight Delay Prediction

We will separate model training and prediction into two parts:
* Training the model offline
* Building a REST API for flight delay prediction using the trained model

## Model Training
* To set up the enviroment for model training, create a virtual environment in Python 3.6 and install the required Python libraries (see `requirements.txt`).
* To train the model, run `python train.py` at the root directory.

## Prediction
* We will use Flask to build a REST API for prediction using the model trained beforehand. The API is designed to accept an example to be predicted. Each API call triggers the feature engineering and prediction process in the machine learning pipeline. 
* This should be fast enough to ensure a real-time response which gives the prediction result in JSON format.
* To run Flask App with Docker, see below.

**Build the docker image**
```
docker build --force-rm=true -t <image tag> .
```

**Run the docker container (if the container is run locally, use 0.0.0.0 for host IP)**
```
docker run -it --publish=<host port>:5000 --name=<container name> -e MODEL_HOST=<host IP> <image tag>
```

**Example query**
```
http://<host IP>:<host port>/prediction?AIRLINE=DL&DAY_OF_WEEK=7&DEPARTURE_TIME=1424.0&DISTANCE=1035
```
