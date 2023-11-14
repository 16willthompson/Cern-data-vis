import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time, glob, os

def dataConf(fileName): 
    # geometry_id,hit_id,channel0,channel1,timestamp,value from file './event000000000-cells.csv'
    data = pd.read_csv(fileName, usecols=['globalX0', 'globalY0', 'globalZ0', 'layerDisk'])

    #conv to df
    df = pd.DataFrame(data,columns=['globalX0', 'globalY0', 'globalZ0', 'layerDisk'])

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

    plt.title(("slice of detector from z: ", sliceStartPoint, "to", sliceStartPoint + sliceStepSize))
    plt.scatter(sliceData['globalX0'], sliceData['globalY0'])

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