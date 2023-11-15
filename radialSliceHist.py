import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time, glob, os

# data configuration and formatting to be sent to plot()
def dataConf(fileName): 
    # read in csv data and spesifiy cols
    data = pd.read_csv(fileName, usecols=['globalX0', 'globalY0', 'globalZ0', 'layerDisk'])

    #conv to df and drop null values 
    df = pd.DataFrame(data,columns=['globalX0', 'globalY0', 'globalZ0', 'layerDisk'])
    df = df.dropna()

    # outputs boundaries of csv data
    print("The bounds for global 0 xyz are: \n"
          "x:", df['globalX0'].min(), df['globalX0'].max(),"\n"
          "y:", df['globalY0'].min(), df['globalY0'].max(),"\n"
          "z:", df['globalZ0'].min(), df['globalZ0'].max(),"\n"
          )

    # user input 
    # does the user want to:
    # spesify z range or slice whole detector
    # slice using phi or eta angle as cutting plane, y/x = phi, x/z = eta
    # speisify radius range to view or leave blank to view whole 

    userInputDict = {}
    userInputDict['zDetectorComp'] = input("Do you want to view Barrel or Disk? Leave blank to spesify range or view whole detector. \n")
    userInputDict['zRange'] = float(input("What z-axis range do you want to view? Leave blank to view whole detector. \n"))
    userInputDict['slicesQuant'] = int(input("How many slices do you want to split the detector into? \n"))
    userInputDict['slicePlane'] = input("What slice plane do you wnat to view? 0 for phi and 1 for eta. \n")
    userInputDict['radusRange'] = int(input("What radius range do you want to view? Leave blank for whole cross section. \n"))


    # arguments for slicing loop
    zAxisRange = abs(df['globalZ0'].max() - df['globalZ0'].min())
    userInputDict['sliceStepSize'] = zAxisRange / userInputDict['slicesQuant']

    # batches main df data into sliced sections to be sent to plot() func
    for userInputDict['slice'] in range(int(df['globalZ0'].min()), int(df['globalZ0'].max())+1, int(userInputDict['sliceStepSize'])):
        sliceData = df[df['globalZ0'].between(userInputDict['slice'], (userInputDict['slice'] + userInputDict['sliceStepSize']) )]
        print("There is", len(sliceData), "points in this slice\n")
        plot(sliceData, userInputDict)


# main plotting funtion, data fed from dataConf()
def plot(sliceData, userInputDict):
    
    # calc angles from positive X-axis for every point then normalise rads between 0 and 2pi
    phiSliceAngles = np.arctan2(sliceData['globalX0'], sliceData['globalY0'])
    phiSliceAngles_Norm = np.mod(phiSliceAngles, 2*np.pi)

    sliceRadius = np.hypot(sliceData['globalX0'], sliceData['globalY0'])

    plotData = {
        'phiAngle': phiSliceAngles_Norm,
        'radius': sliceRadius
    }

    plottingDf = pd.DataFrame(plotData)

    # print df to ee what they are for testing *remove if unneeded
    print("these are the min and max angles:", plottingDf['phiAngle'].min(), plottingDf['phiAngle'].max())
    
    # radial histogram settings 
    histBins = 100
    barBottom = 5
    barWidth = (2*np.pi) / histBins

    radiusLowerBound = 370
    radiusUpperBound = 550

    # left radial histogram
    ax = plt.subplot(121, polar=True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    bars = ax.hist((plottingDf.loc[plottingDf['radius'].between(radiusLowerBound, radiusUpperBound), 'phiAngle']), bins=histBins, width= barWidth, bottom= barBottom)

    # right scatter graph
    ax = plt.subplot(122)
    ax.set_title(("slice of detector from z: " + str(userInputDict['slice']) + " to " + str(userInputDict['slice'] + userInputDict['sliceStepSize'])))
    ax.grid()
    ax.set_xlim(-radiusUpperBound, radiusUpperBound)
    ax.set_ylim(-radiusUpperBound, radiusUpperBound)
    ax.scatter(sliceData.loc[plottingDf['radius'].between(radiusLowerBound, radiusUpperBound), 'globalX0'],
                sliceData.loc[plottingDf['radius'].between(radiusLowerBound, radiusUpperBound),'globalY0']
               )

    # general plt settings for figure formatting 
    plt.rcParams["figure.figsize"] = (16,9)
    plt.tight_layout()
    plt.show()


#user input for file selection
file = input("Path of file to process: \n")
startTime = time.time()

if file == 'del': # delete all files in dir with certain file extention
    for filename in glob.glob('./*.png'):
        os.remove(filename)
elif file != "": # calls dataConf with user input string
    dataConf(file)
else: 
    file = 'stripDataV1.csv' # change this file to change location of datam make sure heading formatting is correct 
    dataConf(file)

# print total time taken (used for benchmarking)
endTime = time.time()
print(endTime-startTime)