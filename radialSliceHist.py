import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# data configuration and formatting to be sent to plot()
def dataConf(fileName): 
    # read in csv data and spesifiy cols
    data = pd.read_csv(fileName, usecols=['globalX0', 'globalY0', 'globalZ0', 'layerDisk', 'eventIndex'])

    #conv to df and drop null values 
    df = pd.DataFrame(data,columns=['globalX0', 'globalY0', 'globalZ0', 'layerDisk', 'eventIndex'])
    df = df.dropna()

    # outputs boundaries of csv data
    print("The bounds for global 0 xyz are: \n"
          "x:", df['globalX0'].min(), df['globalX0'].max(),"\n"
          "y:", df['globalY0'].min(), df['globalY0'].max(),"\n"
          "z:", df['globalZ0'].min(), df['globalZ0'].max(),"\n"
          )
    
    # user input dictinary to store arguments
    userInputDict = {}
    # geometry z-axis tuple ranges. For barrel side A is pos Z, side C is neg Z
    detectorZRange = (-3100, 3100)
    barrelZRange = (-1450, 1450)
    aDiskZRange = (1450, 3100)
    cDiskZRange = (-1450, -3100)

    # barrel or disk, leaving blank for custom range
    userInputDict['zDetectorComp'] = input("Do you want to view Barrel or Disk? Leave blank to specify range or view whole detector. \n").lower()
    if userInputDict['zDetectorComp'] == "barrel":
        userInputDict['zRange'] = barrelZRange
    elif userInputDict['zDetectorComp'] == "disk":
        userInputDict['zDiskSide'] = input("Which set of disks of the detector to view? Positive z-axis or Negative z-axis. \n").lower()

        # set zRange using predefined defaults
        if userInputDict['zDiskSide'] == "positive":
            userInputDict['zRange'] = aDiskZRange
        elif userInputDict['zDiskSide'] == "negative":
            userInputDict['zRange'] = cDiskZRange

    # specify z range or slice whole detector if barrel or disk isnt selected
    if 'zRange' not in userInputDict:
        userInputDict['zRange'] = input("What z-axis range do you want to view? Leave blank to view whole detector. (zMin, zMax) formatting \n")

        # specify radius range to view or leave blank to view whole 
        if userInputDict['zRange'] == "":
            userInputDict['zRange'] = detectorZRange
            userInputDict['slicesQuant'] = int(input("How many slices do you want to split the detector into? \n"))
        else:
            zRangeUISplit = userInputDict['zRange'].split(", ")
            userInputDict['zRange'] = (int(zRangeUISplit[0]), int(zRangeUISplit[1])) 
    
    # slice using phi or eta angle as cutting plane, y/x = phi, x/z = eta
    userInputDict['slicePlane'] = input("What slice plane do you want to view? phi or eta. \n").lower()

    # input for radius range splits string with correct formatting
    userInputDict['radiusRange'] = input("What radius range do you want to view? Leave blank for whole cross section. (rMin, rMax) formatting \n")

    if userInputDict['radiusRange'] == "":
        userInputDict['radiusRange'] = (0, 3200)
    else:
        radiusRangeUISplit = userInputDict['radiusRange'].split(", ")
        userInputDict['radiusRange'] = (int(radiusRangeUISplit[0]), int(radiusRangeUISplit[1]))

    # how many histograms bins the user wants
    userInputDict['histogramBins'] = int(input("How many histogram bins do you want? \n"))

    # automatic slicing after slecting whole dectector 
    if 'slicesQuant' in userInputDict:
        # arguments for slicing loop
        zAxisRange = abs(df['globalZ0'].max() - df['globalZ0'].min())
        userInputDict['sliceStepSize'] = zAxisRange / userInputDict['slicesQuant']

        # batches main df data into sliced sections to be sent to plot() func
        for userInputDict['slice'] in range(int(df['globalZ0'].min()), int(df['globalZ0'].max())+1, int(userInputDict['sliceStepSize'])):
            sliceData = df[df['globalZ0'].between(userInputDict['slice'], (userInputDict['slice'] + userInputDict['sliceStepSize']) )]
            print("There is", len(sliceData), "points in this slice\n")
            plot(sliceData, userInputDict)
    else: # plot user spesified perams
        peramData = df[df['globalZ0'].between(userInputDict['zRange'][0], userInputDict['zRange'][1])]
        print("There is", len(peramData), "points in this slice\n")
        plot(peramData, userInputDict)


# main plotting funtion, data fed from dataConf()
def plot(sliceData, userInputDict):

    #init variables 
    sliceRadius = 0
    sliceAngles = 0

    # calc angles and radii in phi and eta plane slice
    if userInputDict['slicePlane'] == "phi":
        sliceAngles = np.arctan2(sliceData['globalX0'], sliceData['globalY0'])
        sliceRadius = np.hypot(sliceData['globalX0'], sliceData['globalY0'])
    elif userInputDict['slicePlane'] == "eta":
        sliceAngles = np.arctan2(sliceData['globalX0'], sliceData['globalZ0'])
        sliceRadius = np.hypot(sliceData['globalX0'], sliceData['globalZ0'])

    # noramise data and save to df
    sliceAngles_Norm = np.mod(sliceAngles, 2*np.pi)

    plotData = {
        'angle': sliceAngles_Norm,
        'radius': sliceRadius
    }

    plottingDf = pd.DataFrame(plotData)

    # print df to ee what they are for testing *remove if unneeded
    print("These are the min and max angles:", plottingDf['angle'].min(), plottingDf['angle'].max(),
          "\nThere are", len(sliceData['eventIndex'].unique()), "unique eventIndex \n")
    
    # radial histogram settings 
    histBins = userInputDict['histogramBins']
    barBottom = plottingDf['radius'].max()
    barWidth = (2*np.pi) / histBins

    # left radial histogram
    plt.figure("Slice histogram and scatter graph")
    
    ax = plt.subplot(121, polar=True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    bars = ax.hist((plottingDf.loc[plottingDf['radius'].between(userInputDict['radiusRange'][0], userInputDict['radiusRange'][1]), 'angle']), bins=histBins, width= barWidth, bottom= barBottom)

    # right scatter graph
    ax = plt.subplot(122)
    ax.grid()
    # ax.set_xlim(-userInputDict['radiusRange'][1], userInputDict['radiusRange'][1])
    # ax.set_ylim(-userInputDict['radiusRange'][1], userInputDict['radiusRange'][1])
    if userInputDict['slicePlane'] == "phi":
        ax.set_title("slice of detector in phi plane from z: " + str(userInputDict['zRange'][0]) + " to " + str(userInputDict['zRange'][1]))
        ax.scatter(sliceData.loc[plottingDf['radius'].between(userInputDict['radiusRange'][0], userInputDict['radiusRange'][1]), 'globalX0'],
                    sliceData.loc[plottingDf['radius'].between(userInputDict['radiusRange'][0], userInputDict['radiusRange'][1]),'globalY0'])
    elif userInputDict['slicePlane'] == "eta":
        ax.set_title("slice of detector in eta plane from z: " + str(userInputDict['zRange'][0]) + " to " + str(userInputDict['zRange'][1]))
        ax.scatter(sliceData.loc[plottingDf['radius'].between(userInputDict['radiusRange'][0], userInputDict['radiusRange'][1]), 'globalX0'],
                    sliceData.loc[plottingDf['radius'].between(userInputDict['radiusRange'][0], userInputDict['radiusRange'][1]),'globalZ0'])
    
    # plt.figure(1)


    # general plt settings for figure formatting 
    plt.rcParams["figure.figsize"] = (16,9)
    plt.tight_layout()
    plt.show()

#user input for file selection
file = input("Path of file to process: \n")

if file != "": # calls dataConf with user input string
    dataConf(file)
else: 
    file = 'stripDataV1.csv' # change this file to change location of datam make sure heading formatting is correct 
    dataConf(file)