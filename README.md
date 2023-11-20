# Cern-data-vis
Collection of data visualisation programs that read data from [acts-traccc](https://github.com/acts-project/traccc) and athena.

## Table of Contents
* [Setup](#Setup)
* [Organisation](#Organisation)
* [Programs](#Programs)
* [Dependencies](#Dependencies)
* [Licence](#Licence)

## Setup
To get started, clone this repository by doing:
```sh
$ git clone https://github.com/16willthompson/Cern-data-vis
$ pip install -r requirements.txt
```
and thats it, the dependencies are covered [here](#Dependencies).

## Organisation
There is two folders each containing graphing programs based on expected input data:

* `Traccc/` expects .csv data based on the simulation data generated in your traccc/data/tml* folder.
* `ITk/` expects .csv data from athena.

## Programs
Each program varies with ammount of user input requested. Questions are layed out to be self explanitory but in the case of poor graphing performance, try using less extreme values.
### Traccc/ 
#### [clusterFreqImageGen.py](Traccc/clusterFreqImageGen.py)
This file plots the frequency of clusters made by clustering.py, and also displays the average cluster ratio for each geometryID
#### [clustering.py](Traccc/clustering.py)
This program generates a new csv files containing data used to pass into clusterFreqImageGen.py; the input is simulation data from traccc.
#### [imageGen.py](Traccc/imageGen.py)
This program plots all hits on a scatter graph for a given geometryID, or can cycle through all unique IDs.
### ITk/ 
#### [radialSliceHist.py](ITk/radialSliceHist.py)
This program takes in ethena data and plots them using global xyz coords. A number of views can be display and most of what can be changed in the program is given as options in the CLI.
#### [strip3dScatterPlot.py](ITk/strip3dScatterPlot.py)
this is a simple plot of locations of hits in 3d space with an added line that indicates central beamline.
#### [stripFreqChart.py](ITk/stripFreqChart.py)
This is a histogram of phi and eta modules and it can plot the common pairs instead of individual phi and eta.

## Dependencies
Project module dependencies are installed in the [Setup](#Setup) section, and was intended to work on Linux distros. Therefore, some module related linker errors may occur if trying to run on Windows or MacOS.

[Here](requirements.txt) is a file containing a list of all required external (non-default) modules. Newer versions of these modules should work but incase they dont, use the lowest version listed in the document.
## Licence
This project uses the MIT license which can be found in the [license](LICENSE) file, read more at [MIT Wikipedia](https://en.wikipedia.org/wiki/MIT_License).
