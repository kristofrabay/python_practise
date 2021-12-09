# Collection of Python hobby-projects

Main GH repo for any personal / hobby Python project.

## Overview of current projects:
### 1. AirBnB

Using the Inside AirBnB (http://insideairbnb.com/get-the-data.html) data sources, for any city the flow is runable:
- Cleaning & exploration
- Analysis
- Map visualization
- Modeling the price (very difficult to capture, target should be binarized or changed to a i.e.: rating metric)

### 2. LightAutoML

Trying out Russian Сбербанк's AI Lab's automated machine learning library for blackbox models and for whitebox logistic regression using WOE technique


<img src="https://raw.githubusercontent.com/sberbank-ai-lab/LightAutoML/master/imgs/LightAutoML_logo_big.png" width="400"/>

### 3. Scraping projects

Web Scraping using `requests` and `BeautifulSoup` libraries. Scraped sources:
- BKK Futár
- Flightradar24 (limited areas)
- hasznaltauto.hu
- ingatlan.com
- NFL on ESPN 
- Skyscanner (cheap quota collection)
- holtankoljak.hu (gas stations and fuel prices)
- twitter (geo based twitter sentiment)
- South Park (scraping transcripts then running analysis, NLP, etc...)

On top of each scraped source I apply different predictive models. For example for NFL: weekly (regular season) prediction of probability of making it to the Super Bowl

### 4. The Office NLP (also for South Park)

NLP techniques on the entire transcript of The Office series (US). TF-IDF, LDA, networks, sentiment analysis.

### 5. Optimization

PuLP for linear programming, traveling salesman problem (summer vacation optimal round trip model)

### 6. 'Other' stuff
- Price modeling - price elasticity (some basic analysis)
- Old `pandas`, `sklearn` practise scripts
- Py interesting - exploration of some newer / lesser known libraries
- EV (EV data challenge, multiclass classification problem with some TS)