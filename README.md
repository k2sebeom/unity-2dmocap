<p align="center">
    <img src="https://github.com/k2sebeom/unity-2dmocap/blob/master/src/Banner.PNG?raw=true">
</p>

2D Motion Capture for Unity
-------

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/unity-2dmocap.svg)](https://badge.fury.io/py/unity-2dmocap)

**2D Motion Capture for Unity** is a python application designed to be a complement of the Unity asset, 2D Motion Capture.
This asset enables an easy construction of 2D sprite animations in Unity by a completely device-less motion capture technique,
and this application plays a role in analyzing a video file to capture the posture of a human in the video. The extraction of the 
posture from the human image is implemented using [OpenCV](https://opencv.org/) and [torchvision](https://pytorch.org/docs/stable/torchvision/index.html).
With this application, you can easily build a sophisticated animation clip for 
your Unity project without any need of special equipments, and once the animation is
generated, you can freely modify the clips the same way you deal with generic Unity animation.

<p align="center">
        <img src="https://github.com/k2sebeom/unity-2dmocap/blob/master/src/Demo.gif?raw=true" width=500>
</p>

### Features
* Commandline tool for video analysis and a direct connection to Unity Project
* Simple video editor used for preparation of source video
* Extracts human posture using a deep learning model of keypoint RCNN in torchvision
* Exports posture information to a json file
* Generates Unity animation clip on the editor environment
* Easy save & load system for the sprite rigging on Unity

### Installation
```{commandline}
$ pip install unity-2dmocap
```
To update the application to the latest version, you can run:
```{commandline}
$ pip install --upgrade unity-2dmocap
```
To check if the application is installed properly, you can try the following:
```{commandline}
$ python
```
```{python}
>>> import mocap2d
>>> mocap2d.__version__
```
If it prints out something without an error, the application is installed properly.

### Unity Asset

To use this package, you need a 2D Motion Capture asset, which is a counterpart of 
this package. You can find the asset in the Unity Asset Store.

### Usage

Once you have installed the package, you can use the features through a commandline.

```{commandline}
$ 2dmocap-unity [-h] { detect, send } -f FILE [-g] [-i INTERVAL] [-s] [-o OUT]
```
The commands you can use are "detect" and "send". "detect" will analyze the video file
and connect to the Unity project. "send" will read the pre-generated json file
to the Unity Project without an analysis.

If you are using "detect", the arguments are:
* -h, --help: show the help message
* -f FILE, --file FILE: a path to the video file that you want to analyze
* -g, --gpu: with this argument, the program will run on the gpu instance for a fster analysis
* -i INTERVAL, --interval INTERVAL: a target interval between animation keyframes
* -s, --show: with this argument, the program will show the resulting skeleton during the analysis
* -o OUT, -output OUT: a directory in which you will save result.json file for the later use

If you are using "send", the arguments are:
* -f FILE, --file FILE: a path to the json file you want to send

