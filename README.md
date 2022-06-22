# Mnist train and pridict 
---

## Run mnist example from 
### Clone the project
```
git clone https://github.com/tensorflow/serving.git
cd serving
```
### Train in docker
Train (with 100 iterations) and export the first version of model:
```
tools/run_in_docker.sh -d tensorflow/serving:latest-devel python /tensorflow-serving/tensorflow_serving/example/mnist_saved_model.py --training_iteration=100 --model_version=1 /tmp/mnist
```
Train (with 2000 iterations) and export the second version of model:
```
tools/run_in_docker.sh -d tensorflow/serving:latest-devel python /tensorflow-serving/tensorflow_serving/example/mnist_saved_model.py --training_iteration=1000 --model_version=2 /tmp/mnist
```
You should see model created for each training in your /tmp/mnist directory:
```
$ ls /tmp/mnist
1  2
```
### Serve the model
Serving with grpc port 8500 and rest API port 8501:
The easiest way to serve a model is to provide the --model_name and --model_base_path flags:
```
docker run -p 8500:8500 -p 8501:8501 -v /tmp/mnist:/models/mnist -t --entrypoint=tensorflow_model_server tensorflow/serving:latest-devel --enable_batching --port=8500 --rest_api_port=8501 --model_name=mnist --model_base_path=/models/mnist
```
You may provide this configuration file using the --model_config_file flag and instruct Tensorflow Serving to periodically poll for updated versions of this configuration file at the specifed path by setting the --model_config_file_poll_wait_seconds flag.
```
cp $PWD/models.config /tmp/mnist
docker run -p 8500:8500 -p 8501:8501 -v /tmp/mnist:/models/mnist -t --entrypoint=tensorflow_model_server tensorflow/serving:latest-devel --enable_batching --port=8500 --rest_api_port=8501 --model_config_file=/models/mnist/models.config --model_config_file_poll_wait_seconds=60
```
### Make Prediction with grpc request
```
serving/tools/run_in_docker.sh -d tensorflow/serving:latest-devel python /tensorflow-serving/tensorflow_serving/example/mnist_client.py --num_tests=1000 --server=127.0.0.1:8500 --concurrency=10
```
### Get model metadata
```
curl http://localhost:8501/v1/models/mnist
```
---
## Mnist
### Train the model
```
docker run --rm -v $PWD/mnist:/models/mnist tensorflow/serving:latest-devel python /models/mnist/model.py
```
You should see model created for each training in your ./mnist directory:
```
ls mnist
assets  keras_metadata.pb  mnist  model.py  predict.py  sample.json  saved_model.pb  variables
```
### Serve the model
```
docker run -p 8500:8500 -p 8501:8501 -v $PWD/mnist:/models/mnist -t --entrypoint=tensorflow_model_server tensorflow/serving:latest-devel --enable_batching --port=8500 --rest_api_port=8501 -model_name=mnist --model_base_path=/models/mnist
```
### Make Prediction
```
cd mnist
```
Predict with python
```
python predict.py
```
Predict with curl
```
curl -X POST -H "Content-Type: application/json" -d @sample.json 
```
---
## Fashion Mnist
### Train the model
```
docker run --rm -v $PWD/fashion_mnist:/models/mnist tensorflow/serving:latest-devel python /models/mnist/fashion_mnist.py
```
You should see model created for each training in your ./fashion_mnist directory:
```
ls fashion_mnist
assets  fashion_mnist.json  fashion_mnist_predict.py  fashion_mnist.py  keras_metadata.pb  saved_model.pb  variables
```
### Serve the model
```
docker run -p 8500:8500 -p 8501:8501 -v $PWD/fashion_mnist:/models/mnist -t --entrypoint=tensorflow_model_server tensorflow/serving:latest-devel --enable_batching --port=8500 --rest_api_port=8501 -model_name=mnist --model_base_path=/models/mnist
```
### Make Prediction
```
cd fashion_mnist
```
Predict with python
```
python fashion_mnist_predict.py
```
Predict with curl
```
curl -X POST -H "Content-Type: application/json" -d @fashion_mnist.json
```

