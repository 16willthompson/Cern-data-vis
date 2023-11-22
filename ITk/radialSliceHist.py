import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

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
    userInputDict['histogramBins'] = input("How many histogram bins do you want? Leave blank to calc pixelwidth as binsize  \n")

    if userInputDict['histogramBins'] == "":
        userInputDict['pixelBinning'] = int(input("How many pixels do you want to bin together? Input an integer \n"))
    else:
        userInputDict['histogramBins'] = int(userInputDict['histogramBins'])


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
        peramData = df[df['globalZ0'].between(min(userInputDict['zRange']), max(userInputDict['zRange']) )]
        print("There is", len(peramData), "points in this z-axis slice\n")
        plot(peramData, userInputDict)


# main plotting funtion, data fed from dataConf()
def plot(sliceData, userInputDict):
    # ---- Calulations ---- 
    #init variables 
    sliceRadius = 0
    sliceAngles = 0
    slicePlaneAxis = 0

    # calc angles and radii in phi and eta plane slice
    if userInputDict['slicePlane'] == "phi":
        sliceAngles = np.arctan2(sliceData['globalX0'], sliceData['globalY0'])
        sliceRadius = np.hypot(sliceData['globalX0'], sliceData['globalY0'])
        slicePlaneAxis = ('globalX0', 'globalY0')
    elif userInputDict['slicePlane'] == "eta":
        sliceAngles = np.arctan2(sliceData['globalX0'], sliceData['globalZ0'])
        sliceRadius = np.hypot(sliceData['globalX0'], sliceData['globalZ0'])
        slicePlaneAxis = ('globalX0', 'globalZ0')

    # noramise data and save to df
    sliceAngles_Norm = np.mod(sliceAngles, 2*np.pi)

    plotData = {
        'angle': sliceAngles_Norm,
        'radius': sliceRadius
    }

    plottingDf = pd.DataFrame(plotData)

    # filters slice data down to spesified radius range 
    sliceData = sliceData.loc[plottingDf['radius'].between(userInputDict['radiusRange'][0], userInputDict['radiusRange'][1])]

    plottingDf = plottingDf[plottingDf['radius'].between(userInputDict['radiusRange'][0], userInputDict['radiusRange'][1])]
    
    # radial histogram settings 
    radiusAvg = plottingDf['radius'].mean()
    if isinstance(userInputDict['histogramBins'], str):
        # calc number of bins to get binsize the same as a pixel
        radiusCirc = 2 * np.pi * radiusAvg #radcirc in mm 
        histBins = int((radiusCirc / (80e-3)) / userInputDict['pixelBinning']) # 80um for pixel size
    else:
        histBins = userInputDict['histogramBins']
    
    barBottom = radiusAvg
    barWidth = (2*np.pi) / histBins

    # print min and max radii for recording and how many unique event ids, stat summary 
    uniqueEventIndexList = sliceData['eventIndex'].unique()
    radiusMin = plottingDf['radius'].min()
    radiusMax = plottingDf['radius'].max()
    print("These are the min and max radii:", radiusMin, radiusMax, "\n",
          "The average radius is", radiusAvg, "\n",
          "There is", len(plottingDf), "points within spesified radius \n",
          "There are", len(uniqueEventIndexList), "unique eventIndex \n")

    # ---- Plotting ----
    # global perams
    plt.rcParams["figure.figsize"] = (16, 9) 
    plt.rcParams["figure.autolayout"] = True
    scatterPointSize = 5

    # left radial histogram
    plt.figure("Slice histogram and scatter graph")

    ax = plt.subplot(121, polar=True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    values, bins, bars = ax.hist(plottingDf['angle'], bins=histBins, width= barWidth, bottom= barBottom)
    ax.set_ylim(bottom= radiusMin, top= barBottom + values.max() + 2)
    # ax.bar_label(bars, padding=0.1, fontsize=6)

    # right scatter graph
    ax = plt.subplot(122)
    ax.axis('equal')
    ax.grid()
    ax.set_title("slice of detector in " + userInputDict['slicePlane'] + " plane from z: " + str(userInputDict['zRange'][0]) + " to " + str(userInputDict['zRange'][1]))
    ax.scatter(sliceData[slicePlaneAxis[0]],
                sliceData[slicePlaneAxis[1]],
                s=scatterPointSize)
    
    # scatter for showing unique event ids in slice
    plt.figure("Global coordinate scatter with eventIndex colouring")

    ax = plt.subplot(111)
    ax.axis('equal')

    # generate colour list for unique events
    number_of_colors = len(uniqueEventIndexList)
    scatterColor = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                    for i in range(number_of_colors)]

    for index, event in enumerate(uniqueEventIndexList):
        ax.scatter(sliceData.loc[sliceData['eventIndex'] == event, slicePlaneAxis[0]],
                   sliceData.loc[sliceData['eventIndex'] == event, slicePlaneAxis[1]], 
                   c=scatterColor[index], s=scatterPointSize)

    # 2d histogram for phi and eta angles
    # plt.figure(2)
    plt.show()

#user input for file selection
file = input("Path of file to process: \n")

if file != "": # calls dataConf with user input string
    dataConf(file)
else: 
    file = './ITk/stripDataV1.csv' # change this file to change location of datam make sure heading formatting is correct 
    dataConf(file)