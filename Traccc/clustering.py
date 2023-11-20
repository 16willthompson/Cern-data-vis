import pandas as pd
import numpy as np
import math, time, csv

def dataLoad(fileName):

    # geometry_id,hit_id,channel0,channel1,timestamp,value from file './event000000000-cells.csv'
    data = pd.read_csv( './Traccc/' + fileName, usecols=['geometry_id','channel0','channel1','value'])

    #conv to df
    df = pd.DataFrame(data,columns=['geometry_id','channel0','channel1','value'])

    #converts df to list
    geometry_idList = df['geometry_id'].unique().tolist()
    print("unique geometry_id's: " + str(len(geometry_idList)))
    print("most common geometry_id: " + str(df['geometry_id'].mode()))

    # dataBatch = df.loc[df['geometry_id'] == 576460889742380544]

    # clusterData(dataBatch)

    # cluster frequency save location
    clusterQuantitySaveFile = open( './Traccc/' + 'clusterFrequency' + fileName, 'w')
    writer = csv.writer(clusterQuantitySaveFile)
    # headers for csv
    writer.writerow(['geometry_id', 'cluster_quantity', 'avg_cluster_ratio', 'cluster_avg_hits'])

    # cycle through all geometry IDs and retreive cluster qualities, pop ID: 576460889742380544

    writeTimeList = []
    for id in geometry_idList:
        dataBatch = df.loc[df['geometry_id'] == id]
        clusterQualities = clusterData(dataBatch)
        csvWriteStartTime = time.time()
        writer.writerow([str(id), str(clusterQualities[0]), str(clusterQualities[1]), str(clusterQualities[2])])
        csvWriteEndTime = time.time()
        writeTimeList.append(csvWriteEndTime-csvWriteStartTime)

    print("avg time per line write: " + str(sum(writeTimeList)/len(writeTimeList)) + ", total time for writing " + str(len(writeTimeList)) + " lines: " + str(sum(writeTimeList)))
    clusterQuantitySaveFile.close()


def distance(x1, y1, x2, y2):
    return abs(math.sqrt( (x1-x2)**2 + (y1-y2)**2 ))

def centeroidnp(arr):
    arr = np.array(arr)
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length

def aspectRatio(min, max):
    width = abs(min[0] - max[0])
    height = abs(min[1] - max[1])
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    return (height/width)

def clusterData(data):

    xList = data['channel0'].values.tolist()
    yList = data['channel1'].values.tolist()

    currentCluster = []
    allClusters = []

    for i in range(len(xList)-1):
        currentPoint = (xList[i], yList[i])

        nextNodeDist = distance(xList[i], yList[i], xList[i+1], yList[i+1])

        if nextNodeDist <= 2:
            currentCluster.append(currentPoint)
        elif nextNodeDist > 2:
            currentCluster.append(currentPoint)
            allClusters.append(currentCluster)
            currentCluster = []
    
    avgRatio = 0
    clusterAvgHits = 0


    for cluster in allClusters:
        # print(centeroidnp(cluster))
        avgRatio += aspectRatio(min(cluster),max(cluster))
        clusterAvgHits += len(cluster)

    if len(allClusters) == 0:
        avgRatio = (avgRatio/(len(allClusters)+1))
        clusterAvgHits = (clusterAvgHits / (len(allClusters)+1))
    else:
        avgRatio = (avgRatio/len(allClusters))
        clusterAvgHits = (clusterAvgHits / len(allClusters))

    return len(allClusters), avgRatio, clusterAvgHits



file = input("Path of file to process, blank for default or del to delete previous files*: ")

startTime = time.time()

if file == "":
    dataLoad('event000000000-cells.csv')
else: 
    dataLoad(file)

endTime = time.time()
print(endTime-startTime)