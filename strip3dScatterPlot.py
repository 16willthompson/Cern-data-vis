import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time, glob, os

def dataConf(fileName): 
    # geometry_id,hit_id,channel0,channel1,timestamp,value from file './event000000000-cells.csv'
    data = pd.read_csv(fileName, usecols=['eventIndex', 'localX', 'localY', 'localZ'])

    #conv to df
    df = pd.DataFrame(data,columns=['eventIndex', 'localX', 'localY', 'localZ'])

    #passes df to plotting func
    uniqueEventList = df['eventIndex'].unique().tolist()
    del uniqueEventList[0]
    print("there are ", len(uniqueEventList), " unique event ids")
    print("highest frequency event index: " + str(df['eventIndex'].mode()))
    
    limitsMargin = 25

    for id in uniqueEventList:
        dataBatch = df.loc[df['eventIndex'] == id]
        # xlims = (dataBatch['localX'].min() - limitsMargin, dataBatch['localX'].max() + limitsMargin)
        # ylims = (dataBatch['localY'].min() - limitsMargin, dataBatch['localY'].max() + limitsMargin)
        # zlims = (dataBatch['localZ'].min() - limitsMargin, dataBatch['localZ'].max() + limitsMargin)
        plot(dataBatch, limitsMargin)

def plot(data, margin):
    # configures dataframe data into python lists
    localXList = list(data.iloc[:, 1])
    localYList = list(data.iloc[:, 2])
    localZList = list(data.iloc[:, 3])

    xlims = (data['localX'].min() - margin, data['localX'].max() + margin)
    ylims = (data['localY'].min() - margin, data['localY'].max() + margin)
    zlims = (data['localZ'].min() - margin, data['localZ'].max() + margin)
    
    # create artifical beamline 
    beamDensisity = 50

    zLimRange = zlims[1] - zlims[0]
    beamStep = zLimRange/beamDensisity

    beamXList = [0] * beamDensisity
    beamYList = [0] * beamDensisity
    beamZList = []

    beamZMaxTemp = zlims[1]

    for i in range(beamDensisity):
        beamZList.append(beamZMaxTemp)
        beamZMaxTemp -= beamStep


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(localXList, localYList, localZList, c='r', marker='o')
    ax.scatter(beamXList, beamYList, beamZList, c='b', marker='o')

    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_zlim(zlims)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax.set_title("event id: " + str(int(data['eventIndex'].iloc[0])))
    # plt.
    plt.tight_layout()
    # plt.savefig("./stripHistImages/" + str(int(data['eventIndex'].iloc[0])) + '.pdf', bbox_inches='tight')
    plt.show()

#user input for file selection
file = input("Path of file to process: ")
startTime = time.time()

if file == 'del': # delete all files in dir with certain file extention
    for filename in glob.glob('./*.png'):
        os.remove(filename)
else: 
    file = 'stripDataV1.csv'
    dataConf(file)

endTime = time.time()
print(endTime-startTime)