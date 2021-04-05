import yfinance as yf
import pickle
import datetime
import random


def randomDate():
    year = random.randint(2019, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.date(year=year, month=month, day=day)


def dateToString(date):
    return date.strftime('%Y-%m-%d')


def getTickerHistory(tickerName, date, dayInterval, interval):
    delta = datetime.timedelta(days=dayInterval)
    ticker = yf.Ticker(tickerName)
    history = ticker.history(start=dateToString(date - delta), end=dateToString(date), interval=interval)
    pickle.dump(history, open(f"{tickerName.upper()}History{date.strftime('%Y_%m_%d')}_{interval}.p", "wb"))
    return history


actualDate = randomDate()

SPYHistory = getTickerHistory("SPY", actualDate, 2, "1h")

print(SPYHistory)
# print(SPYHistory.loc["2005-05-02"])

