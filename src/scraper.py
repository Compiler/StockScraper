import sys, getopt, logging, requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.DEBUG)### CRITICAL debug WARNING INFO DEBUG NOTSET



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

def parse_content(html_data):
    dom_struct = BeautifulSoup(html_data, 'html.parser')
    table_class = "snapshot-table2"
    table_row = "table-dark-row"
    match = dom_struct.find_all("table", {"class":table_class})
    print(match[0].text)


def scrape_url(url):
    logging.critical("Scraping '%s'", url)
    data = validate_url(url)#retrieve html data
    if(data[0] == -1): return
    parse_content(data[1])
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
        logging.debug('test.py -i <inputfile>')
        sys.exit(2)

    #execute tickers scrape
    for cur_url in open(input_file, "r", encoding="utf-8"):
        scrape_url(base_url + cur_url)
