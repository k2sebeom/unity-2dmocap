<img src="https://github.com/k2sebeom/unity-2dmocap/blob/master/src/Banner.PNG?raw=true" align=center></img>

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

### Usage


