# StockScraper
Scrapes data for tickers

## First time use


```
> git clone git@github.com:Compiler/StockScraper.git
> cd StockScraper
> pip install -r requirements.txt
> python src\scraper.py
```

## Using with custom input


```
> python src\scraper.py -i my_input_file_with_list_of_tickers.py
```

Your input file should name a ticker followed by a new line for each ticker. If it's just one ticker, it doesn't need a new line.
