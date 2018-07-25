# Build SSD-MobileNet Object Detector with Customized dataset on iOS + CoreML

## Introduction 

An implemetation of training object detector on **iOS** by using [Tensorflow Object API](https://github.com/tensorflow/models/tree/master/research/object_detection) that can detect multiple obejects we defined.

The tools using here are **CoreML + Tensorflow** rather than **Tensorflow lite**.
Building Tensorflow lite library in iOS is also an option, which will be implemented in the future.

Training on a special dataset [UEC food 256](http://foodcam.mobi/dataset256.html) to detect the position of food. You can create your customized dataset and recognized them in your iPhone.

Note that coreML should build with iOS 11 or higher. 
 

## Building Steps : 

1.   [Installing Tensorflow-GPU and the Tensorflow Object Detection API](#installing-tensorflow-gpu-and-the-tensorflow-object-detection-api)
2.   [Preparation for our own data](#preparation-for-our-own-data)
3.   [Label the bounding box for each category](#label-and-bounding-box-for-each-category)
4.   [Generating training data](#generating-training-data)
5.   [Create Label Map and configuring training](#create-label-map-and-configuring-training)
6.   [Training and Evaluation](#training-and-evaluation)
7.   [Exporting the inference graph](#exporting-the-inference-graph)
8.   [Create an iOS App with Xcode-Project](#ceate-an-ios-app-with-xcode-project)
9.   [CoreML : turning frozen graph to mlmodel](#coreml-:-turning-frozen-graph-to-mlmodel)
10. [Testing your own object detector in iPhone](#testing-your-own-object-detector-in-iphone)

Note that CoreML requires iOS 11 or higher version. I'm running on Ubuntu 16.0.1 with python 3.6.

## Installing Tensorflow GPU and the Tensorflow Object Detection API

Installing tensorflow with gpu version , the version I used is 1.7.1, the newer version should work though.


First of all : 
```
# From tensorflow/models/research/
protoc object_detection/protos/*.proto --python_out=.
```

Please run through the [installation instructions](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) to install Tensorflow and all its dependencies. Ensure the Protobuf libraries are compiled and the library directories are added to `PYTHONPATH`.

```
# From tensorflow/models/research/
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```

Testing buld:
```
python3 object_detection/builders/model_builder_test.py
```

Note that we need to clone [tensorflow-model](https://github.com/tensorflow/models/tree/ea6d6aabe5c121102a645d3f08cf819fa28d2a03/research
) first. See [Note](#note).

## Preparation for our own data

In order to train a detector, we require a dataset of images, bounding boxes and classifications.
The data directory should appear as follows, containg raw images and annotation.

```
+ annotations/ : contains the xml files in PASCAL VOC format
+ images/      : contains the image that you'd like to train on.
+ data/        : contains the input file for the TF object detection API and the label files (csv)
  -label_map file
  -train TFRecord file
  -eval TFRecord file
  -train.csv
  -eval.csv
+ models/      : contains the pipeline configuration file, frozen model and labelmap
  + model
   -pipeline config file
   +train
   +eval
```
I'm creating dataset with some modification by referencing [this](https://github.com/datitran/raccoon_dataset), which is very useful.


## Label and bounding box for each category

We can use [labelImg](https://github.com/tzutalin/labelImg) to label the location of each object.
[labelImg](https://github.com/tzutalin/labelImg) would generate .xml file in PASCAL VOC format for each iamge.

Using [transfer_to_xml.py](scripts/transfer_to_xml.py). to generate xml file for each image. 

Note that before we label the bounding box, split dataset into train/test set. 


### Recommended Directory Structure for Training and Evaluation
[Running Locally](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_locally.md)


## Generating training data  

- tfrecords : Before turn the xml into tfrecord, lets see the correctness of our xml. First of all, [transfer xml into csv file]().
If there's nothing wrong, we can see a green rectangle that bounds the object.

### Split data into train/val and testing
May reference [Here](scripts/split_to_train_test_cvs.py).


## Create Label Map and configuring training

Configure [this](training/ssd_mobilenet_v1_pets.config). 
1. num_ class
2. path of checkpoints ,tfrecord, and label map.

[Label Map](data/object-detection.pbtxt) look like this.

## Training and Evaluation

See [Note](#note).

## Exporting the inference graph

See [Note](#note).

## Create an iOS App with Xcode-Project

## CoreML : turning frozen graph to mlmodel 

## Testing your own object detector in iPhone


## Note :
 Since there are so many versions of tensorflow object detection API, I'll record what should do in different version.

### 1. Version with train.py & eval.py

This is the version that I used for training, it's evaluation mode is some how conflict with training. 
The eval error message is like :  0 difficut flag / Not found calss [ 0  2 4 6 8 ], something like that, which still remain unsolved through google.
However, the thing that we trained somehow seems working.

In this version, we use command like down below :

Training : 

```
python3 object_detection/train.py --train_dir=../../../food_data/x_training/model  --pipeline_config_path=../../../food_data/x_training/faster_rcnn_inception_v2.config 
```

Exporting the model :

```
python3 object_detection/export_inference_graph.py --input_type image_tensor --pipeline_config_path ../../../food_data/x_training/faster_rcnn_inception_v2.config  --trained_checkpoint_prefix ../../../food_data/x_training/model/model.ckpt-40082 --output_directory ../../../food_data/x_training/model/inference_graph
```

### 2. Master Version (2018.07) with model_main.py

The master version avoids the problem of conflict with evalation since it do training and evaluation at the same time. 
However, both of training and evaluation use GPU, which causes very long context swtich time. 

In this version, we use command like down below :

Training and Evalating  :

```
 python3 object_detection/model_main.py --pipeline_config_path=../../../food_data/724models/ssd_mobilenet_v1_pets.config --model_dir=../../../food_data/724models/ --num_train_steps=50000 --num_eval_steps=6000  --alsologtostderr
```

Note that the eval steps should be the same amount as you testing set.

### Using Tensorboard : 

Every version can use tensorboard with following:

```
tensorboard --logdir=${DIR_OF_model-xxxx.ckpt}
```


