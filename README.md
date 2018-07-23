# Dash-DAQ-Omega-PID

## Introduction
An application to control the [CN32PT-440-DC Omega PID Controller](https://www.omega.ca/pptst_eng/CNPT_SERIES.html)! [Play with the demo](https://dash-daq-omega-pid.herokuapp.com/) and learn more about this application from our [blog entry](https://www.dashdaq.io/control-an-led-strip-in-python). // Enter blog entry

### Propotional, Integral, Derivative Gain Controller (PID Controller)
PID controllers are widely used in closed loop control systems. A closed loop control system has an input that is reliant on the output of the system.  This process is known as [feedback](https://en.wikipedia.org/wiki/Feedback). In this system the desired output is defined as the setpoint, where the difference bewteen the setpoint and actual output, defines the error of the system. This error is what is known as the feedback, and is than looped back to the input, in what is known as the feedback loop. Now the proportional, integral, and derivative gains, and error are using in the PID equation to solve for the percentage of output applied to the system to reach the setpoint ([refer to mathamatical form](https://en.wikipedia.org/wiki/PID_controller). For more information and detail on this system please refer [here](https://en.wikipedia.org/wiki/PID_controller)
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
* Reset: Reset graph.
* PID%: The percentage of output applied to system.
* C°: Current temperature.
* Manual (Boolean Switch): Switch to manual tuning PID.
* Autotune (Boolean Switch): Switch to autotuning PID.
* Autotune Timeout: Timeout for autotuning period.
* PID Setpoint: The desired output to reach.
* Max Rate (/min): Maximum rate of change per miniute.
* Proportional Gain: The proportional gain of the controller.
* Derivative Gain: The derivate gain of the controller.
* Integral Gain: The integral gain of the controller.
* Out 1: Output on/off.
* Set PID (Button): Set PID parameters in manual.
* Autotune (Button): Start Autotune, for optimized PID parameters.
* Adaptive Control: Fuzzy logic control more [here](https://www.omega.ca/technical-learning/pid-fuzzy-logic-adaptive-control.html)
* Couple: The thermocouple type used.
* Refresh: Refresh rate of graph.
* Filter Rate: Sensitivity of thermocouple.
* Action Mode: Heating, cooling, or heating and cooling system. 
* PID: The output is dependent on the PID parameters.
* Start: Start PID controller and graphing data.
* Stop: Stop PID controller and stop graphing data.

## Resources
This application was controlled through the MODBUS, using the minimalmodbus library, which can be found [here](http://minimalmodbus.readthedocs.io/en/master/apiminimalmodbus.html). In order to determine outputs, inputs, and any other information related to the controller refer to the manual [here](https://www.omega.com/manuals/manualpdf/M5451.pdf). For a list of commands that can be written/read to the controller refer to the MODBUS manual [here](https://www.omega.com/manuals/manualpdf/M5458.pdf)

