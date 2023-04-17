import pandas as pd

SnP500List = pd.read_html(r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
ignoreExtra = SnP500List[0] # stores only S&P 500 component stocks; ignores extra info
tickerList = ignoreExtra[['Symbol']].sort_values(by=['Symbol'], ascending=True)
tickerList.to_csv(r'S&P 500\S&P500.csv', index=False)