from io import StringIO
from time import sleep
import requests
import pandas as pd
from  datetime import datetime, timedelta
import bs4


head = {
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
}

class GetData():
    session = None
    ticker = None

    def __init__(self, ticker, 
                 from_date=(datetime(datetime.today().year - 1, datetime.today().month,datetime.today().day).strftime("%d-%m-%Y")),
                 to_date=(datetime.today().strftime("%d-%m-%Y"))
             ):
        self.session = requests.session()
        self.ticker=ticker
        self.from_date=from_date
        self.to_date=to_date
        self.df=pd.DataFrame()
        
    def getHistoryData(self):
        '''
        Check if timeframe is over 2 years because NSE does not allow more
        than 2 years at a time
        '''
        from_date = datetime.strptime(self.from_date, "%d-%m-%Y")
        to_date = datetime.strptime(self.to_date, "%d-%m-%Y")
        diff = to_date.year - from_date.year
        if diff<=2:
            self.df = self.getEquityData(self.from_date, self.to_date)
            return self.df

        for i in range(0,int(diff/2)+1):
            d = to_date.year - (i+1)*2
            if d < from_date.year:
                d = from_date.year 

            date1=datetime(d, from_date.month, from_date.day).strftime("%d-%m-%Y")
            date2=datetime(to_date.year - i*2, to_date.month, to_date.day).strftime("%d-%m-%Y")
            dataframe = self.getEquityData(date1, date2)
            self.df = self.df.append(dataframe)
            sleep(1)
        self.save_csv()

    def getEquityData(self, from_date, to_date):
        self.session.get("https://www.nseindia.com", headers=head)
        self.session.get("https://www.nseindia.com/get-quotes/equity?symbol=" + self.ticker, headers=head)  # to save cookies
        self.session.get("https://www.nseindia.com/api/historical/cm/equity?symbol="+self.ticker, headers=head)
        url = "https://www.nseindia.com/api/historical/cm/equity?symbol=" + self.ticker + \
            "&series=[%22EQ%22]&from=" + from_date + \
            "&to=" + to_date + "&csv=true"
        webdata = self.session.get(url=url, headers=head)
        dataframe = pd.read_csv(StringIO(webdata.text[3:]))
        return dataframe

    def niftyHistoryData(self):
        varient = self.ticker.upper().replace(' ', '%20').replace('-', '%20')
        webData = self.session.get(
            url="https://www1.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType=" + varient + "&fromDate=" + self.from_date + "&toDate=" + self.to_date,
            headers=head)
        soup = bs4.BeautifulSoup(webData.text, 'html5lib')
        self.df = pd.read_csv(StringIO(soup.find('div', {'id': 'csvContentDiv'}).contents[0].replace(':','\n')))
        return self.df
    
    def filter_data(self):
        dataframe = self.df
        dataframe['OPEN '] = dataframe['OPEN '].replace('\D', '', regex=True).astype(int)/100
        dataframe['HIGH '] = dataframe['HIGH '].replace('\D', '', regex=True).astype(int)/100
        dataframe['LOW '] = dataframe['LOW '].replace('\D', '', regex=True).astype(int)/100
        dataframe['PREV. CLOSE '] = dataframe['PREV. CLOSE '].replace('\D', '', regex=True).astype(int)/100
        dataframe['ltp '] = dataframe['ltp '].replace('\D', '', regex=True).astype(int)/100
        dataframe['close '] = dataframe['close '].replace('\D', '', regex=True).astype(int)/100
        dataframe['vwap '] = dataframe['vwap '].replace('\D', '', regex=True).astype(int)/100
        dataframe['52W H '] = dataframe['52W H '].replace('\D', '', regex=True).astype(int)/100
        dataframe['52W L '] = dataframe['52W L '].replace('\D', '', regex=True).astype(int)/100
        dataframe['VALUE '] = dataframe['VALUE '].replace('\D', '', regex=True).astype(int)/100
        self.df = dataframe

    def save_csv(self):
        if not self.df.empty:
            self.filter_data()
            self.df.to_csv('csv/'+self.ticker+'.csv',index=False)


tcs_data = GetData('TCS', from_date='14-05-2015', to_date='14-05-2022')
tcs_data.getHistoryData()
# tcs_data.save_csv()
# print(niftyHistoryData('NIFTY 50'))


def getId(name):
    search_url = 'https://www.nseindia.com/api/search/autocomplete?q={}'
    get_details = 'https://www.nseindia.com/api/quote-equity?symbol={}'
    session.get('https://www.nseindia.com/', headers=head)
    search_results = session.get(url=search_url.format(name), headers=head)
    search_result = search_results.json()['symbols'][0]['symbol']

    company_details = session.get(url=get_details.format(search_result), headers=head)
    return company_details.json()['info']['identifier']

# getId('tata motors') => TATAMOTORSEQN
