import pandas as pd
class DataStore:
    def __init__(self):
        self.dataframe = pd.DataFrame()

    def addToData(self, data):
        self.dataframe = self.dataframe.append(data, sort = False)

    def createDataFrameCorrectShape(self):
        raise Exception("Depreciated")
        data = {'Date': [], 'Con': [], 'Lab': [], 'Lib Dem': [], 'Brexit Party': [], 'SNP': [], 'Palid Cymru': [],
                'Green': [], 'torytotory': [],
                'torytolab': [], 'torytolibdem': [], 'labtotory': [], 'labtolab': [], 'labtolibdem': []}
        return pd.DataFrame(data)


