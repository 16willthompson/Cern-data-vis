# Cern-data-vis
Collection of data visualisation programs that read data from [cern-acts-traccc](https://github.com/acts-project/traccc) and athena.

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
#### [clustering.py](Traccc/clustering.py)
#### [imageGen.py](Traccc/imageGen.py)
### ITk/ 
#### [radialSliceHist.py](ITk/radialSliceHist.py)
#### [strip3dScatterPlot.py](ITk/strip3dScatterPlot.py)
#### [stripFreqChart.py](ITk/stripFreqChart.py)
## Dependencies
Project module dependencies are installed in the [Setup](#Setup) section, and was intended to work on Linux distros. Therefore, some module related linker errors may occur if trying to run on Windows or MacOS.

[Here](requirements.txt) is a file containing a list of all required external (non-default) modules. Newer versions of these modules should work but incase they dont, use the lowest version listed in the document.
## Licence
This project uses the MIT license which can be found in the [license](LICENSE) file, read more at [MIT Wikipedia](https://en.wikipedia.org/wiki/MIT_License).
