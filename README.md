# Requirement for FG2000-scrapy
- You need Anaconda python package manager [Python version 3.6]

- Scrapy (A web scrapper tool) directly available on Anaconda via package manager. [Scrapy version 1.3.3]

- Convert csv to excel ipython notebook is still work-in-progess but it works. I'm still working on optimising the code and customising spreadsheet.


To run the code you need to use command prompt (cmd/terminal) pointing to the project folder

Scrapy provide 3 output formats - [xml, json, csv] - To create one of your choice type below code on terminal
- "scrapy crawl fg2000 -t xml -o fg2000.xml"
- "scrapy crawl fg2000 -t json -o fg2000.json"
- "scrapy crawl fg2000 -t csv -o fg2000.csv"
