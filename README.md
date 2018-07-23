# Dash-DAQ-Omega-PID

## Introduction
An application to control the [CN32PT-440-DC Omega PID Controller](https://www.omega.ca/pptst_eng/CNPT_SERIES.html)! [Play with the demo](https://dash-daq-omega-pid.herokuapp.com/) and learn more about this application from our [blog entry](https://www.dashdaq.io/control-an-led-strip-in-python). // Enter blog entry

### Propotional, Integral, Derivative Gain Controller (PID Controller)


### dash-daq
[Dash DAQ](http://dash-daq.netlify.com/#about) is a data acquisition and control package built on top of Plotly's [Dash](https://plot.ly/products/dash/). It gives users more accesibility and, key features for data aquistion applications.


## Requirements
It is advisable	to create a separate conda environment running Python 3 for the app and install all of the required packages there. To do so, run (any version of Python 3 will work):

```
conda create -n	[your environment name] python=3.6.4
```
```
source activate [your environment name]
```

To install all of the required packages to this conda environment, simply run:

```
pip install -r requirements.txt
conda install -c poehlmann python-seabreeze
```

and all of the required `pip` packages, as well as the //Have to test this method// package, will be installed, and the app will be able to run.
 
## How to use the app
Here, you should put the command needed to run your app, and then the steps that the user should take to use it. You should include screenshots of the app running in your own browser to make it easier to follow along. 

Then, show a step-by-step guide of how your app works, and what each control does.

If possible, include screenshots of something in the app failing, and, if any, the steps that the user can take to correct the error.

There are two versions of this application. A mock version for the user to play with without any instruments connected, and a local version, that can be connected to a device.

If you would like to run the local version, please connect the device to the USB port on your computer, and run in the command line:
``` 
python app.py
```

If the app is run, but the device is not connected you will see something like this:



If you would like to run the mock version, run in the command line:

```
python app_mock.py demo
```
A step by step guide with photos is provided below:
### Controls
* On/Off: Turn Blinkstick LED's on or off. 
* LED Select: Select individual LED's and change their color, with the color picker.
* All: Select all LED's and modify their colors simutaneously, with the color picker.
* Rainbow: All LED's light up according to the rainbow color spectrum.
* LED Slider: Turn on LED's one through to the selection on the slider, and change the color with color picker.
* Color Picker: Change the color of the LED/LED's to the color selected.


## Resources
The Blinkstick API is used in this application, and has a ton of features. If you need some help figuring out the Blinkstick API check out the documentation [here](https://www.blinkstick.com/documentation/python/frames.html). Too install the Blinkstick API go [here](https://github.com/arvydas/blinkstick-python). If you have trouble using the API with Python 3, check out this [fix](https://github.com/arvydas/blinkstick-python/issues/34)

