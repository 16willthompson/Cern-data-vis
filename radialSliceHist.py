import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time, glob, os

def dataConf(fileName): 
    # geometry_id,hit_id,channel0,channel1,timestamp,value from file './event000000000-cells.csv'
    data = pd.read_csv(fileName, usecols=['globalX0', 'globalY0', 'globalZ0', 'layerDisk'])

    #conv to df
    df = pd.DataFrame(data,columns=['globalX0', 'globalY0', 'globalZ0', 'layerDisk'])

    df = df.dropna()

    #passes df to plotting func
    print("The bounds for global 0 xyz are: \n"
          "x:", df['globalX0'].min(), df['globalX0'].max(),"\n"
          "y:", df['globalY0'].min(), df['globalY0'].max(),"\n"
          "z:", df['globalZ0'].min(), df['globalZ0'].max(),"\n"
          )

    slicesQuant = int(input("how many slices do you want to split the detector into? "))
    zAxisRange = abs(df['globalZ0'].max() - df['globalZ0'].min())
    sliceStepSize = zAxisRange / slicesQuant

    for slice in range(int(df['globalZ0'].min()), int(df['globalZ0'].max())+1, int(sliceStepSize)):
        sliceData = df[df['globalZ0'].between(slice, (slice + sliceStepSize) )]
        plot(sliceData, slice, sliceStepSize)


def plot(sliceData, sliceStartPoint, sliceStepSize):
    
    phiSliceAngles = np.arctan2(sliceData['globalX0'], sliceData['globalY0'])

    phiSliceAngles_Norm = np.mod(phiSliceAngles, 2*np.pi)

    print(phiSliceAngles_Norm, "\n",
          "this is the max and min angles:", phiSliceAngles_Norm.max(), phiSliceAngles_Norm.min())
    
    # radial histogram settings 
    histBins = 20
    barBottom = 10

    maxBarHeight = 6
    barWidth = (2*np.pi) / histBins

    # left radial histogram
    ax = plt.subplot(121, polar=True)
    bars = ax.hist(phiSliceAngles_Norm, width= barWidth, bottom= barBottom)

    # right scatter graph
    ax = plt.subplot(122)
    ax.set_title(("slice of detector from z: " + str(sliceStartPoint) + " to " + str(sliceStartPoint + sliceStepSize)))
    ax.scatter(sliceData['globalX0'], sliceData['globalY0'])

    plt.rcParams["figure.figsize"] = (16,9)
    plt.tight_layout()
    plt.show()





#user input for file selection
file = input("Path of file to process: \n")
startTime = time.time()

if file == 'del': # delete all files in dir with certain file extention
    for filename in glob.glob('./*.png'):
        os.remove(filename)
elif file != "":
    dataConf(file)
else: 
    file = 'stripDataV1.csv' # change this file to change location of datam make sure heading formatting is correct 
    dataConf(file)

endTime = time.time()
print(endTime-startTime)