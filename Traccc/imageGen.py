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
    print("Unique geometry_id's: " + str(len(geometry_idList)))
    print("Most common geometry_id: " + str(df['geometry_id'].mode()))

    # user input questions 
    userInputDict = {}
    userInputDict['generateAllGeoIDs'] = input("Specify GeoID to plot or leave blank to do all unique GeoIDs: \n")
    userInputDict['savePlotImage'] = input("Do you want to save the plot as an image? (yes/no) \n").lower()
    userInputDict['viewPlots'] = input("Do you want to view all plots as they are generated? (yes/no) \n").lower()
    userInputDict['printRunTime'] = input("do you want to view the ammount of time taken per plot? (yes/no) \n").lower

    #checks if user has specified GeoID, if not do all unique ids

    if userInputDict['generateAllGeoIDs'] == "":
        for id in geometry_idList:
            ProcessStartTime = time.time()
            dataBatch = df.loc[df['geometry_id'] == id]
            toImage(dataBatch, id, userInputDict)
            ProcessEndTime = time.time()
            if userInputDict['printRunTime'] == "yes":
                print(ProcessEndTime - ProcessStartTime)
    else:
        userInputDict['generateAllGeoIDs'] = int(userInputDict['generateAllGeoIDs'])
        dataBatch = df.loc[df['geometry_id'] == userInputDict['generateAllGeoIDs']]
        toImage(dataBatch, userInputDict['generateAllGeoIDs'], userInputDict)

# function to plot data and save to file 
def toImage(data, geo_id, userInputDict):
    xMax = 1500 #channel0
    yMax = 500 #channel1

    # generate blank binary image 
    imageArray = np.zeros((yMax, xMax), dtype=int)

    #generate hits in binary image
    for _,hit in data.iterrows():
        imageArray[int(hit['channel0']), int(hit['channel1'])] = 1

    # plt setup
    plt.figure(figsize=(12,6))
    plt.xlim(0, xMax)
    plt.ylim(0, yMax)
    plt.title('Sensor hits on ID: ' + str(geo_id))
    plt.imshow(imageArray, cmap='gray_r', interpolation='none')
    plt.grid()
    plt.tight_layout()
    # checks if user wants to save all plots
    if userInputDict['savePlotImage'] == "yes":
        plt.savefig("./geoidimages/" + str(geo_id) + '.pdf', bbox_inches='tight')
    if userInputDict['viewPlots'] == "yes":
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
print("Total time taken:", endTime-startTime)