import requests
import json
import numpy as np
from tensorflow.keras.datasets.mnist import load_data

#load MNIST dataset
(_, _), (x_test, y_test) = load_data()

# reshape data to have a single channel
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2], 1))
# normalize pixel values
x_test = x_test.astype('float32') / 255.0

def make_prediction(instances):
   data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
   with open("sample.json", "w") as outfile:
     outfile.write(data)
   headers = {"content-type": "application/json"}
   json_response = requests.post('http://localhost:8501/v1/models/mnist/versions/4:predict', data=data, headers=headers)
   print(json_response.status_code)
   predictions = json.loads(json_response.text)['predictions']
   return predictions
   
predictions = make_prediction(x_test[0:1])
#predictions = make_prediction(x_test[:20])
for pred in predictions:
    print(np.argmax(pred))

for i, pred in enumerate(predictions):
    print(f"True Value: {y_test[i]}, Predicted Value: {np.argmax(pred)}")

