from io import StringIO
import requests
import pandas as pd
from  datetime import datetime , timedelta
import bs4

session = requests.session()
head = {
    # 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 "
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
}


def getHistoryData(company, from_date=(datetime.today().strftime("%d-%m-%Y")), to_date=(datetime(datetime.today().year - 1, datetime.today().month,datetime.today().day).strftime("%d-%m-%Y"))):
    print(from_date,to_date)
    session.get("https://www.nseindia.com", headers=head)
    session.get("https://www.nseindia.com/get-quotes/equity?symbol=" + company, headers=head)  # to save cookies
    session.get("https://www.nseindia.com/api/historical/cm/equity?symbol="+company, headers=head)
    url = "https://www.nseindia.com/api/historical/cm/equity?symbol=" + company + "&series=[%22EQ%22]&from=" + from_date + "&to=" + to_date + "&csv=true"
    webdata = session.get(url=url, headers=head)
    df = pd.read_csv(StringIO(webdata.text[3:]))
    return df

# print(getHistoryData('SHREECEM',from_date='30-04-2020',to_date='30-04-2021'))

def niftyHistoryData(varient, from_date = ((datetime(datetime.today().year - 1, datetime.today().month, datetime.today().day) + timedelta(days=2)).strftime("%d-%m-%Y")), to_date =(datetime.today().strftime("%d-%m-%Y"))):
    varient = varient.upper()
    varient = varient.replace(' ', '%20')
    varient = varient.replace('-', '%20')
    webData = session.get(
        url="https://www1.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType=" + varient +
            "&fromDate=" + from_date + "&toDate=" + to_date,
        headers=head)
    soup = bs4.BeautifulSoup(webData.text, 'html5lib')
    df = pd.read_csv(StringIO(soup.find('div', {'id': 'csvContentDiv'}).contents[0].replace(':','\n')))
    df.to_csv('csv/'+varient+'.csv',index=False)
    return df


print(niftyHistoryData('NIFTY 50'))
