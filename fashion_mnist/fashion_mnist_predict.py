import random
import json
import requests
import numpy as np
from tensorflow import keras
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# scale the values to 0.0 to 1.0
train_images = train_images / 255.0
test_images = test_images / 255.0

# reshape for feeding into the model
train_images = train_images.reshape(train_images.shape[0], 28, 28, 1)
test_images = test_images.reshape(test_images.shape[0], 28, 28, 1)

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

print('\ntrain_images.shape: {}, of {}'.format(train_images.shape, train_images.dtype))
print('test_images.shape: {}, of {}'.format(test_images.shape, test_images.dtype))

#take 3 pictures for inference
data = json.dumps({"signature_name": "serving_default", "instances": test_images[0:3].tolist()})
#print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))
#print(data)
with open("fashion_mnist.json", "w") as outfile:
  outfile.write(data)
# docs_infra: no_execute
headers = {"content-type": "application/json"}
json_response = requests.post('http://localhost:8501/v1/models/fashion_model/versions/5:predict', data=data, headers=headers)
print(json_response, json_response.text)
predictions = json.loads(json_response.text)['predictions']

for i in range(0,3):
    print (np.argmax(predictions[i]), class_names[test_labels[i]])
