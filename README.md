# Cern-data-vis
Collection of data visualisation programs that read data from [cern-acts-traccc](https://github.com/acts-project/traccc) and athena.

## Table of Contents
* [Setup](#Setup)
* [Requirements](#Requirements)
* [Organisation](#Organisation)
* [Programs](#Programs)
* [Dependencies](#Dependencies)
* [Licence](#Licence)

## Setup
To get started, clone this repository by doing:
'''sh
git clone https://github.com/16willthompson/Cern-data-vis
pip install -r requirements.txt
'''
and thats it, the dependencies are covered in the [Requirements](#Requirements) section.
## Requirements

## Organisation
There is two folders each containing graphing programs based on expected input data:

* 'Traccc/' expects .csv data based on the simulation data generated in your traccc/data/tml* folder.
* 'ITk/' expects .csv data from athena.

## Programs

## Dependencies
Project module dependencies are installed int the [Setup](#Setup) section, and was intended to work on Linux distros therefore some module related errors may occur if trying to run on Windows or MacOS.

[Here](requirements.txt) is a file containing a list of all required external (non-default) modules. Newer versions of these modules should work but incase they dont, use the lowest version listed in the document.
## Licence
This project uses the MIT license which can be found in the [license](LICENSE) file, read more at [MIT Wikipedia](https://en.wikipedia.org/wiki/MIT_License).
