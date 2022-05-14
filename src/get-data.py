from io import StringIO
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

    def getHistoryData(self):
        self.session.get("https://www.nseindia.com", headers=head)
        self.session.get("https://www.nseindia.com/get-quotes/equity?symbol=" + self.ticker, headers=head)  # to save cookies
        self.session.get("https://www.nseindia.com/api/historical/cm/equity?symbol="+self.ticker, headers=head)
        url = "https://www.nseindia.com/api/historical/cm/equity?symbol=" + self.ticker + "&series=[%22EQ%22]&from=" + self.from_date + "&to=" + self.to_date + "&csv=true"
        webdata = self.session.get(url=url, headers=head)
        df = pd.read_csv(StringIO(webdata.text[3:]))
        df.to_csv('csv/'+self.ticker+'.csv',index=False)
        return df

    def niftyHistoryData(self):
        varient = self.ticker.upper().replace(' ', '%20').replace('-', '%20')
        webData = self.session.get(
            url="https://www1.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType=" + varient +
                "&fromDate=" + self.from_date + "&toDate=" + self.to_date,
            headers=head)
        soup = bs4.BeautifulSoup(webData.text, 'html5lib')
        df = pd.read_csv(StringIO(soup.find('div', {'id': 'csvContentDiv'}).contents[0].replace(':','\n')))
        df.to_csv('csv/'+ticker+'.csv',index=False)
        return df


tcs_data = GetData('TCS', from_date='14-05-2020', to_date='14-05-2022')
print(tcs_data.getHistoryData())
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
