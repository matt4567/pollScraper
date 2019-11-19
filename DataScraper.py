import tabula
import pandas as pd
from DataStore import DataStore
class DataScraper:
    def __init__(self, dataStore):
        #I'm not entirely sure what this should do
        self.dataStore = dataStore
        self.newData = pd.DataFrame()
        return

    def scrapeData(self, poller):
        if poller == "yougov":
            df = tabula.read_pdf("pollData.pdf", area = [252,170, 400, 400], pages='1')
            # df.drop(0, inplace=True)

            dataList = df.values.tolist()
            dataFrameCols = [x[0] for x in dataList]
            dataFrameVals = [x[2] for x in dataList]

            date = self.getDate(poller)
            dataFrameCols.insert(0, "Date")
            dataFrameVals.insert(0, date)
            cleanedDataFrame = pd.DataFrame(dataFrameVals).T
            cleanedDataFrame.columns = dataFrameCols
            self.newData = cleanedDataFrame

    def getDate(self, poller):
        if poller == "yougov":
            df = tabula.read_pdf("pollData.pdf", area=[90, 100, 130, 190], pages='1')
            return df.values.tolist()[0][0]

    def saveToDataStore(self):
        self.dataStore.addToData(self.newData)

    def scrapeFlowData(self, poller):
        if poller == "yougov":
            df = tabula.read_pdf("pollData.pdf", area = [140,420, 400, 600], pages='3')
            flowList = df.values.tolist()
            flowListCleaned = [flowList[0][0], flowList[0][1], flowList[0][2], flowList[1][0], flowList[1][1], flowList[1][2]]
            flowListDataFrame = pd.DataFrame(flowListCleaned).T
            flowListColumns = ['torytotory', 'torytolab', 'torytolibdem', 'labtotory', 'labtolab', 'labtolibdem']
            flowListDataFrame.columns = flowListColumns
            self.newData = pd.concat([self.newData, flowListDataFrame], axis=1)

dataStore = DataStore()
dataScraper = DataScraper(dataStore)
dataScraper.scrapeFlowData("yougov")
dataScraper.scrapeData("yougov")
dataScraper.saveToDataStore()
print(dataStore.dataframe)