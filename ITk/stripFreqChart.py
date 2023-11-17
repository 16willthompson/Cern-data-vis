import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time, glob, os

def dataConf(fileName): 
    # geometry_id,hit_id,channel0,channel1,timestamp,value from file './event000000000-cells.csv'
    data = pd.read_csv(fileName, usecols=['instance', 'charge', 'etaModule', 'eventIndex', 'layerDisk', 'phiModule', 'strip'])

    #conv to df
    df = pd.DataFrame(data,columns=['instance', 'charge', 'etaModule', 'eventIndex', 'layerDisk', 'phiModule', 'strip'])

    #passes df to plotting func
    uniqueEventList = df['eventIndex'].unique().tolist()
    del uniqueEventList[0]
    print("there are ", len(uniqueEventList), " unique event ids")
    print("highest frequency event index: " + str(df['eventIndex'].mode()))
    print(" the lowest eta and phi are", df['etaModule'].min(), df['phiModule'].min(), "and the largest eta and phi are", df['etaModule'].max(), df['phiModule'].max())
    
    YNCombinedModules = str(input("Do you want combined modules Y or N? "))

    # print(df[['etaModule', 'phiModule']].value_counts().reset_index(name='count'))

    # print("second method ", df.groupby(['etaModule','phiModule']).size())

    plot(df, YNCombinedModules)

    for id in uniqueEventList:
        dataBatch = df.loc[df['eventIndex'] == id]
        # dataBatch.drop(index=dataBatch.index[0], axis=0, inplace=True)
        plot(dataBatch, YNCombinedModules)

# outputting plots and creating axis data
def plot(data, combineQ):
    # configures dataframe data into python lists
    instanceCol = list(data.iloc[:, 0])
    chargeCol = list(data.iloc[:, 1])
    etaModuleCol = list(data.iloc[:, 2])
    eventIDCol = list(data.iloc[:, 3])
    layerCol = list(data.iloc[:, 4])
    phiModuleCol = list(data.iloc[:, 5])
    stripCol = list(data.iloc[:, 6])

    # dictionaries to group data
    etaStats = {}
    phiStats = {}

    # for each row in data, add to dictionary with metrics
    for row in range(len(instanceCol)):
        id = str(etaModuleCol[row]) + " " + str(phiModuleCol[row])

        if str(etaModuleCol[row]) == 'nan' or str(phiModuleCol[row]) == 'nan':
            continue

        etaVal = str(etaModuleCol[row])
        phiVal = str(phiModuleCol[row])

        if combineQ == "N":
            if etaVal in etaStats:
                etaStats[etaVal] = [etaStats[etaVal][0] + 1, etaStats[etaVal][1] + chargeCol[row]]
            else:
                etaStats[etaVal] = [1, chargeCol[row]]

            
            if phiVal in phiStats:
                phiStats[phiVal] = [phiStats[phiVal][0] + 1, phiStats[phiVal][1] + chargeCol[row]]
            else:
                phiStats[phiVal] = [1, chargeCol[row]]

        else:
            if id in etaStats:
                etaStats[id] = [etaStats[id][0] + 1, etaStats[id][1] + chargeCol[row]]
            else:
                etaStats[id] = [1, chargeCol[row]]
            
    # frequency of each event 
    if combineQ == "Y":
        for event in eventIDCol:
            currEvent = str(event)

            if currEvent == 'nan':
                pass
            else:
                if currEvent in phiStats:
                    phiStats[currEvent] = [phiStats[currEvent][0] + 1]
                else:
                    phiStats[currEvent] = [1]

    # remove null values 
    if 'nan nan' in etaStats:
        del etaStats['nan nan']
    if 'nan' in etaStats:
        del etaStats['nan']
    if 'nan' in phiStats:
        del phiStats['nan']

    # put dict keys into list to be read by plt
    etaXLabels = list(etaStats.keys())
    etaFreq = []

    phiXLabels = list(phiStats.keys())
    phiFreq = []

    # dict values with corresponding index with axis label
    for item in etaXLabels: 
        etaFreq.append(etaStats[item][0])

    for item in phiXLabels:
        phiFreq.append(phiStats[item][0])
    
    if combineQ == "Y" or combineQ == "y":
        fig, axis = plt.subplots(2)
        # graph setup for unique event ids
        axis[0].set_title("frequency of unique event ids")
        axis[0].bar(phiXLabels, phiFreq, width=0.8)

        # graph setup for common pairs
        print("this is how many common pairs there are: ", len(etaXLabels))
        axis[1].set_title("frequency of combined modules against eta and phi")
        axis[1].bar(etaXLabels, etaFreq, width=0.8)

        # add radial histogram based on phi and eta modules 
        # ax = plt.subplot(111, polar=True)
        # bars = ax.bar(phiXLabels, phiFreq, width=0.8) 
        # plt.show()

    else: 
        fig, axis = plt.subplots(2)
        # per event frequency graph setup 
        axis[0].set_title("hits deposited for each eta module")
        axis[0].bar(etaXLabels, etaFreq, width=0.8)

        axis[1].set_title("hits deposited for each phi module")
        axis[1].bar(phiXLabels, phiFreq, width=0.8)

    # plt show setup
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
    file = 'stripDataV1.csv' # change this file to change location of datam make sure heading formatting is correct 
    dataConf(file)

endTime = time.time()
print(endTime-startTime)