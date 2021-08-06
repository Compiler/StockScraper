import sys, getopt, logging, requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.DEBUG)### CRITICAL debug WARNING INFO DEBUG NOTSET
import json


def validate_url(test_url):
        try:
            res = requests.get(str(test_url), headers= {'User-Agent' : "Mozilla/5.0"})
            if(res.status_code != 200):
                logging.warn("Failed to load '%s' -- response code : %s", test_url, str(res.status_code))
                if(res.status_code == 429):
                    logging.debug("Sleeping")
                    time.sleep(5)
                    logging.debug("Reattempting connection!")
                    return validate_url(test_url) #recurse
                return [-1, -1]
            logging.debug("Validated URL")
            return [1, res.content]
        except requests.exceptions.Connectiondebug:
            logging.debug("Connection Exception caught")
            return validate_url(test_url) #recurse

def parse_content(html_data, ticker):
    dom_struct = BeautifulSoup(html_data, 'html.parser')
    table_class = "snapshot-table2"
    table_row = "table-dark-row"
    match = dom_struct.find_all("table", {"class":table_class})
    print(match[0].text)
    brute_force_parse_data(match[0].text, ticker)

def brute_force_parse_data(data, ticker):
    titles = ["Index", "P/E", "EPS (ttm)", "Insider Own", "Shs Outstand", "Perf Week",
                "Market Cap", "Forward P/E", "EPS next Y", "Insider Trans", "Shs Float", "Perf Month",
                "Income", "PEG", "EPS next Q", "Inst Own", "Short Float", "Perf Quarter",
                "Sales", "P/S", "EPS this Y", "Inst Trans", "Short Ratio", "Perf Half Y",
                "Book/sh", "P/B", "EPS next Y", "ROA", "Target Price", "Perf Year", 
                "Cash/sh", "P/C", "EPS next 5Y", "ROE", "52W Range", "Perf YTD", 
                "Dividend", "P/FCF", "EPS past 5Y", "ROI", "52W High", "Beta",
                "Dividend %", "Quick Ratio", "Sales past 5Y", "Gross Margin", "52W Low", "ATR",
                "Employees", "Current Ratio", "Sales Q/Q", "Oper. Margin", "RSI (14)", "Volatility",
                "Optionable", "Debt/Eq", "EPS Q/Q", "Profit Margin", "Rel Volume", "Prev Close",
                "Shortable", "LT Debt/Eq", "Earnings", "Payout", "Avg Volume", "Price",
                "Recom", "SMA20", "SMA50", "SMA200", "Volume", "Change"]

    #handles the n-1 cases
    print("================================================\n", ticker)
    m_dict = {
        "ticker": ticker
    }
    last_find = 0
    for cur_pos in range(0, len(titles)):
        next_pos = cur_pos + 1
        if(next_pos >= len(titles)): break
        start_pos = data.find(titles[cur_pos], last_find)
        end_pos = data.find(titles[next_pos], last_find)

        offset = len(titles[cur_pos])

        last_find = start_pos + offset
        header = titles[cur_pos].strip("\n ")
        value = data[start_pos + offset:end_pos].strip("\n ")
        m_dict[header] = value
        print(header, ":", value)
        if(end_pos == -1 or start_pos == -1): exit();

    #handle last case
    cur_pos = len(titles)-1
    start_pos = data.find(titles[cur_pos])
    offset = len(titles[cur_pos])
    header = titles[cur_pos].strip("\n ")
    value = data[start_pos + offset:].strip("\n ")
    print(header, ":", value)
    m_dict[header] = value
    with open("ticker_data.json", "a+") as outfile: 
        json.dump(m_dict, outfile)
        outfile.write('\n')


def scrape_url(url, ticker):
    logging.critical("Scraping '%s'", url)
    data = validate_url(url)#retrieve html data
    if(data[0] == -1): return
    parse_content(data[1], ticker)
    pass


if __name__ == '__main__':
    base_url = "https://finviz.com/quote.ashx?t="

    #command line parse
    try:
        opts, args = getopt.getopt(sys.argv,"hi:o:",["ifile="])
        if(len(args) < 2):
            input_file = "default_input_file.txt"
        else:
            input_file = args[-1]
        logging.debug(input_file)
    except getopt.Getoptdebug:
        logging.debug('src/scraper.py -i <inputfile>')
        sys.exit(2)

    #execute tickers scrape
    for cur_url in open(input_file, "r", encoding="utf-8"):
        scrape_url(base_url + cur_url, cur_url.strip('\n '))
