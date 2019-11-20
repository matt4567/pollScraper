import tabula
import utils
import pandas as pd
import PyPDF2
from DataStore import DataStore
class DataScraper:
    def __init__(self, dataStore, src):
        #I'm not entirely sure what this should do
        self.dataStore = dataStore
        self.newData = pd.DataFrame()
        self.fileLoc = src
        self.flowList = self.readPDFForFlows()
        return


    def scrapeData(self, poller):
        if poller == "yougov":
            df = tabula.read_pdf(self.fileLoc, area = [252,170, 400, 400], pages='1')
            # df.drop(0, inplace=True)
            index = self.findCorrectNumbers(df)
            df = self.cleanData(df)
            dataList = df.values.tolist()
            dataFrameCols = [x[0] for x in dataList]
            dataFrameVals = [x[index] for x in dataList]

            date = self.getDate(poller)
            dataFrameCols.insert(0, "Date")
            dataFrameVals.insert(0, date)
            cleanedDataFrame = pd.DataFrame(dataFrameVals).T
            cleanedDataFrame.columns = dataFrameCols
            print(cleanedDataFrame)
            self.buildUpCurrentDataFrame(cleanedDataFrame)


    def findCorrectNumbers(self, df):
        list = df.values.tolist()
        count = 0
        i= 0
        for val in list:
            try:
                int(val[i])
                if count == 1:
                    return i
                count +=1
            except:
                i+=1
                continue
            i+=1

    def cleanData(self, df):
        for index, row in df.iterrows():
            if utils.isNan(row[2]):
                df = df.drop(index)
        return df

    def buildUpCurrentDataFrame(self, df):
        self.newData = pd.concat([self.newData, df], axis = 1)


    def getDate(self, poller):
        if poller == "yougov":
            df = tabula.read_pdf(self.fileLoc, area=[90, 95, 130, 190], pages='1')
            returnVal = df.values.tolist()[0][0]
            while returnVal[0] == "-":
                returnVal = returnVal[1:]
            return returnVal

    def saveToDataStore(self):
        self.dataStore.addToData(self.newData)

    def scrapeFlowData(self, poller):
        if poller == "yougov":
            df = tabula.read_pdf(self.fileLoc, area = [140, 420, 400, 600], pages='3')
            flowList = df.values.tolist()
            print(df)
            flowListCleaned = [flowList[0][0], flowList[0][1], flowList[0][2], flowList[1][0], flowList[1][1], flowList[1][2]]
            flowListDataFrame = pd.DataFrame(flowListCleaned).T
            flowListColumns = ['torytotory', 'torytolab', 'torytolibdem', 'labtotory', 'labtolab', 'labtolibdem']
            flowListDataFrame.columns = flowListColumns
            print(flowListDataFrame)
            self.buildUpCurrentDataFrame(flowListDataFrame)

    def getRightPage(self):
        pageNum = 0
        pdfFileObj = open(self.fileLoc, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        returable = False

        while returable == False:
            pageObj = pdfReader.getPage(pageNum)
            text = pageObj.extractText()
            if "general election" in text:
                returable = True
            else:
                pageNum += 1
        return pageNum+1


    def readPDFForFlows(self):
        pageN = self.getRightPage()
        df = tabula.read_pdf(self.fileLoc, area=[120, 250, 500, 600], pages=pageN)
        return df.values.tolist()

    def getsFlowsStartIndex(self):
        for indexBig, valBig in enumerate(self.flowList):
            for indexSmall, valSmall in enumerate(valBig):
                try:
                    testVal = int(valSmall)
                except:
                    continue
                if testVal == 100:
                    try:
                        if int(self.flowList[indexBig+1][indexSmall+1]) == 100 and int(self.flowList[indexBig+2][indexSmall+2]) == 100:
                            additional = 1
                            val = int(self.flowList[indexBig][indexSmall+additional])
                            while(val == 0):
                                additional+=1
                                val = int(self.flowList[indexBig][indexSmall + additional])
                            return indexBig, indexSmall + additional
                    except:
                        continue



    def getFlows(self):
        y, x = self.getsFlowsStartIndex()
        data = self.flowList
        flows = [data[y][x], data[y+1][x], data[y+2][x], data[y+3][x], data[y+4][x], data[y+5][x], data[y+6][x], data[y+7][x]
            , data[y+8][x], data[y+9][x], data[y+10][x], data[y][x+1], data[y+1][x+1], data[y+2][x+1], data[y+3][x+1],
                 data[y+4][x+1], data[y+5][x+1], data[y+6][x+1], data[y+7][x+1], data[y+8][x+1], data[y+9][x+1], data[y+10][x+1],
                 data[y][x+2], data[y+1][x+2], data[y+2][x+2], data[y+3][x+2], data[y+4][x+2], data[y+5][x+2], data[y+6][x+2],
                 data[y+7][x+2], data[y+8][x+2], data[y+9][x+2], data[y+10][x+2]]

        dataframeFromList = self.convertToDataFrame(flows)
        self.buildUpCurrentDataFrame(dataframeFromList)


    def convertToDataFrame(self, flows):
        dataFrame = pd.DataFrame(flows).T
        columns = ['t2t', 't2l', 't2lib', 't2snp', 't2pc', 't2brex', 't2green', 't2sop', 't2no', 't2dk', 't2r',
                   'l2t', 'l2l', 'l2lib', 'l2snp', 'l2pc', 'l2brex', 'l2green', 'l2sop', 'l2no', 'l2dk', 'l2r',
                   'lib2t', 'lib2l', 'lib2lib', 'lib2snp', 'lib2pc', 'lib2brex', 'lib2green', 'lib2sop', 'lib2no', 'lib2dk',
                   'lib2r']
        dataFrame.columns = columns
        return dataFrame


dataStore = DataStore()
dataScraper = DataScraper(dataStore, "pollData4.pdf")
dataScraper.getFlows()
# dataScraper.scrapeFlowData("yougov")
dataScraper.scrapeData("yougov")
print(dataStore.dataframe)
dataScraper.getFlows()
dataScraper.saveToDataStore()

print(dataStore.dataframe)