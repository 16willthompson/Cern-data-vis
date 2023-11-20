import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time, glob, os

def dataConf(fileName): 
    # geometry_id,hit_id,channel0,channel1,timestamp,value from file './event000000000-cells.csv'
    data = pd.read_csv(fileName, usecols=['geometry_id', 'cluster_quantity', 'avg_cluster_ratio', 'cluster_avg_hits'])

    #conv to df
    df = pd.DataFrame(data,columns=['geometry_id', 'cluster_quantity', 'avg_cluster_ratio', 'cluster_avg_hits'])

    #converts df to list
    geometry_idList = df['geometry_id'].unique().tolist()
    print("unique geometry_id's: " + str(len(geometry_idList)))
    print("most common geometry_id: " + str(df['geometry_id'].mode()))

    plot(df)

def plot(data):
    # configures dataframe data into python lists
    geometryIds = list(data.iloc[:, 0])
    clusterFreq = list(data.iloc[:, 1]) 
    avgClusterRatio = list(data.iloc[:, 2]) 
    clusterAvgHits = list(data.iloc[:, 3])

    geoIDsLen = len(geometryIds)

    volumeDict = {} # 0: cluster frequency, 1: cluster xy ratio, 2: avg hits per cluster, 3 how many accounts of that volume there is in data 
    layerDict = {} # 0: cluster frequency

    #cycle through geo IDs to add volume and layer keys to dictionaries then add all colliding values 
    for i in range(geoIDsLen):
        geometryIds[i] = hex(geometryIds[i])
        currVolume = geometryIds[i][2:4]
        currLayer = geometryIds[i][6:9]
        # input data into dictionary, if key is already in dic it adds already stored value with new value, else puts new value in place
        if currVolume in volumeDict:
            volumeDict[currVolume] = [
                                    volumeDict[currVolume][0] + clusterFreq[i],
                                    volumeDict[currVolume][1] + avgClusterRatio[i],
                                    volumeDict[currVolume][2] + clusterAvgHits[i],
                                    volumeDict[currVolume][3] + 1
                                    ]
        else:
            volumeDict[currVolume] = [clusterFreq[i], avgClusterRatio[i], clusterAvgHits[i],1]

        if currLayer in layerDict:
            layerDict[currLayer] = layerDict[currLayer] + clusterFreq[i]
        else:
            layerDict[currLayer] = clusterFreq[i]


    volumeX = list(volumeDict.keys())
    volumeYFreq = []
    volumeYAvgRatio = []
    volumeYClusterHits = []

    for item in volumeDict:
        #averaging the grouped averages 
        volumeDict[item] = [volumeDict[item][0], (volumeDict[item][1]/volumeDict[item][3]), (volumeDict[item][2]/volumeDict[item][3])]

        #setting up axis values
        volumeYFreq.append(volumeDict[item][0])
        volumeYAvgRatio.append(volumeDict[item][1])
        volumeYClusterHits.append(volumeDict[item][2])

    # plotting settings 
    fig, axis = plt.subplots(2,2)

    axis[0,0].set_title("GeoID volume cluster frequency")
    axis[0,0].bar(volumeX,volumeYFreq, width=0.8)

    layerX = list(layerDict.keys())
    layerY = list(layerDict.values())

    axis[1,0].set_title("GeoID layer")
    axis[1,0].bar(layerX, layerY, width=0.8)

    axis[0,1].set_title("GeoID volume avg hits per cluster")
    axis[0,1].bar(volumeX, volumeYClusterHits, width=0.8)

    axis[1,1].set_title("GeoID volume avg xy ratio of cluster")
    axis[1,1].bar(volumeX, volumeYAvgRatio, width=0.8)

    plt.tight_layout()
    plt.show()    

#user input for file selection
file = input("Path of file to process: ")
startTime = time.time()

if file == 'del': # delete all files in dir with certain file extention
    for filename in glob.glob('./*.png'):
        os.remove(filename)
else: 
    file = './Traccc/clusterFrequencyevent000000000-cells.csv'
    dataConf(file)

endTime = time.time()
print(endTime-startTime)