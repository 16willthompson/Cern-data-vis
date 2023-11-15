import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time, glob, os

def dataConf(fileName): 
    # geometry_id,hit_id,channel0,channel1,timestamp,value from file './event000000000-cells.csv'
    data = pd.read_csv(fileName, usecols=['geometry_id','channel0','channel1','value'])

    #conv to df
    df = pd.DataFrame(data,columns=['geometry_id','channel0','channel1','value'])

    #converts df to list
    geometry_idList = df['geometry_id'].unique().tolist()
    print("unique geometry_id's: " + str(len(geometry_idList)))
    print("most common geometry_id: " + str(df['geometry_id'].mode()))

    dataBatch = df.loc[df['geometry_id'] == 576460889742380544]

    toImage(dataBatch, 576460889742380544)

    #iterate through all unique geometry ids and call toImage func 576460889742380544
    # for id in geometry_idList:
    #     ProcessStartTime = time.time()
    #     dataBatch = df.loc[df['geometry_id'] == id]
    #     toImage(dataBatch, id)
    #     ProcessEndTime = time.time()
    #     print(ProcessEndTime - ProcessStartTime)


def dfs(pixel,imageArray, visited):
    stack = []
    if pixel not in visited and imageArray[pixel[0]][pixel[1]] == 1:
        visited.append(pixel)
        for yCheck in range(-1,2):
            for xCheck in range(-1,2):
                if yCheck != 0 and xCheck != 0:
                    currPixel = (pixel[0]+xCheck,pixel[1]+yCheck)
                    if imageArray[currPixel] == 1 and [currPixel] not in visited:
                        print("test check " + str(currPixel))
                        stack.append(currPixel)
                        dfs(currPixel, imageArray, visited)
    
    # print("currnt stack before loop: " + str(stack))
    # for newPixel in stack:
    #     dfs(newPixel, imageArray, visited)
    # print("currnt stack after loop: " + str(stack))
    # stack.clear()
    print("inside loop" + str(visited) + " this is the stack " + str(stack))
    return stack

def toImage(data, geo_id):
    xMax = 1500 #channel0
    yMax = 500 #channel1

    # generate blank binary image 
    imageArray = np.zeros((yMax, xMax), dtype=int)

    visited = []

    #generate hits in binary image
    for _,hit in data.iterrows():
        imageArray[int(hit['channel0']), int(hit['channel1'])] = 1

    # search neighboring points for connections 
    # for _,hit in data.iterrows():
    #     visited = dfs([int(hit['channel0']), int(hit['channel1'])], imageArray, visited)
    #     print("outside loop" + str(visited))

    # visited = dfs([int(hit['channel0']), int(hit['channel1'])], imageArray, visited)
    # print("outside loop" + str(visited))

    plt.figure(figsize=(10,6))
    plt.xlim(0, xMax)
    plt.ylim(0, yMax)
    plt.title('Sensor hits on ID: ' + str(geo_id))
    plt.imshow(imageArray, cmap='gray_r', interpolation='none')
    plt.grid()
    # plt.savefig("./images/" + str(geo_id) + '.pdf', bbox_inches='tight')
    plt.show()

#user input for file selection
file = input("Path of file to process, blank for default or del to delete previous files*: ")
startTime = time.time()
if file == "":
    dataConf('./event000000000-cellstml200.csv') #default file selection
elif file == 'del':
    for filename in glob.glob('./*.png'):
        os.remove(filename)
else: 
    dataConf(file)

endTime = time.time()
print(endTime-startTime)