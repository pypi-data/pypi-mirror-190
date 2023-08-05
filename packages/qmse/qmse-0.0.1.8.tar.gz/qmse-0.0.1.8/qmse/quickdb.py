import pickle, datetime, time
import numpy as np
import pandas as pd
import os
import json

def save_pkl(data, dest):
    with open(dest, 'wb') as f:
        pickle.dump(data, f)

def load_pkl(dest):
    try:
        with open(dest, 'rb') as f:
            return pickle.load(f)
    except:
        return None

def load_json(dest):
    try:
        with open(dest, 'rb') as f:
            return json.load(f)
    except:
        return None

path = "S:/all member/퀀트운용팀/93 QuickDB/"

class QuickDB:
    def __init__(self, yqtb=None, fsdata=None, path=None):
        if path is None:
            self.path = "S:/all member/퀀트운용팀/93 QuickDB/"
        else:
            self.path = path
        if yqtb is None or fsdata is None:
            self.refresh()
        else:
            self.yqtb = yqtb
            self.fsdata = fsdata
        

    def refresh(self): # daily update하면 refresh 해줘야함.
        self.yqtb = load_pkl(os.path.join(self.path, 'yq.table'))
        self.fsdata = load_pkl(os.path.join(self.path, 'fsdata.data'))
        
    def getYQ(self, when):
        return self.yqtb.loc[:str(when)].iloc[-1]

    def getFS(self, account, date, tickers=None):
        result = {}
        for ticker, yq in db.getYQ(date).dropna().iteritems():
            result[ticker] = fsdata[yq][account].get(ticker)
        if tickers is not None:
            return pd.Series(result)[tickers]
        else:
            return pd.Series(result)

    def getTradables(self, date):
        return self.getTS(88, self).where(lambda x : x == 0).dropna()

    def _getTrailingYQ(self, yq, n=4):
        y,q = yq[:4], (yq[4:])
        roll = ['03' , '06', '09', '12']

        while roll[0] != q:
            roll = np.roll(roll, 1)

        YQ = [y+q]

        for i in range(n-1):
            roll = np.roll(roll, 1)
            if roll[0] == '12':
                y = str(int(y) - 1)
            q = roll[0]
            YQ.append(y+q)
        return YQ

    def getTrailingFS(self, account, date, n=4, method=None):
        YQ = self.getYQ(date).dropna().map(lambda x : self._getTrailingYQ(x, n))
        res = {}
        for ticker, yq in YQ.iteritems():
            try:
                res[ticker] = pd.Series(
                    self.fsdata[_yq][account].get(ticker) for _yq in yq
                )
            except:
                pass
        df = pd.DataFrame(res).dropna(axis=1)

        if method == 'sum':
            return df.sum()
        if method == 'std':
            return df.std()
        if method == 'mean':
            return df.mean()
        else:
            return df


    def getTS(self, n, start:str, end:str=None):
        start = str(start)
        end = str(end)
        y1 = int(str(start)[:4])
        res = []
        try:
            if end:
                y2 = int(str(end)[:4])
                for y in range(y1, y2+1):
                    _ = load_pkl(os.path.join(self.path, f"data/{y}_{n}.data"))
                    if _ is not None:
                        res.append(_)
                return pd.concat(res).sort_index().loc[start : end]
            else:
                return load_pkl(os.path.join(self.path, f'data/{y1}_{n}.data')).loc[start]
            #.sort_index().drop_duplicates().loc[start:].iloc[0]
        except Exception as e:
            print(e)
            return None